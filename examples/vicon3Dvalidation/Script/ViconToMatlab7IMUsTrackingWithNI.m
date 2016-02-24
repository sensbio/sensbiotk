clear all;
close all;

% Load the SDK
fprintf( 'Loading SDK...' );
Client.LoadViconDataStreamSDK();
fprintf( 'done\n' );

% Load the NI board config
daq.getVendors()
daq.getDevices()

session = daq.createSession('ni');
session.Rate = 100;
session.addAnalogInputChannel('Dev2','ai0','Voltage'); %log the aiO voltage channel

% Program options
HostName = 'localhost:801';
% HostName = '127.0.0.1';

% Make a new client
MyClient = Client();

% Connect to a server
fprintf( 'Connecting to %s ...', HostName );
while ~MyClient.IsConnected().Connected
    % Direct connection
    MyClient.Connect( HostName );
    fprintf( '.' );
end
fprintf( '\n' );

% Enable some different data types
MyClient.EnableSegmentData();
MyClient.EnableDeviceData();
MyClient.EnableMarkerData();
MyClient.EnableUnlabeledMarkerData();

% Set the streaming mode
MyClient.SetStreamMode( StreamMode.ClientPull );

MyClient.SetAxisMapping( Direction.Forward, ...
    Direction.Left,    ...
    Direction.Up );    % Z-up

% A dialog to stop the loop
MessageBox = msgbox( 'Stop DataStream Client', version );

% Objects
Object1 = 'LEFT_FOOT';
Object2 = 'LEFT_SHANK';
Object3 = 'RIGHT_FOOT';
Object4 = 'RIGHT_SHANK';
Object5 = 'BACK';
Object6 = 'LEFT_THIGH';
Object7 = 'RIGHT_THIGH';

% Prepare files and headers
file1 = fopen(strcat('Results\',Object1,'.txt'),'w');
fprintf(file1,'Tracker Experiment Results ') ;
fprintf(file1, [date '\r\n']);
fprintf(file1, [Object1 '\r\n']);
fprintf(file1, '\t Translation \t\t\t Local Quaternion \t\t\t\t Local EulerXYZ \t\t\t\r\n ');
fprintf(file1,'%s\t %s\t %s\t %s\t %s\t %s\t %s\t %s\t %s\t %s\t %s\t\r\n','t','x','y','z','x','y','z','w','x','y','z');

file2 = fopen(strcat('Results\',Object2,'.txt'),'w');
fprintf(file2,'Tracker Experiment Results ') ;
fprintf(file2, [date '\r\n']);
fprintf(file2, [Object2 '\r\n']);
fprintf(file2, '\t Translation \t\t\t Local Quaternion \t\t\t\t Local EulerXYZ \t\t\t\r\n ');
fprintf(file2,'%s\t %s\t %s\t %s\t %s\t %s\t %s\t %s\t %s\t %s\t %s\t\r\n','t','x','y','z','x','y','z','w','x','y','z');

file3 = fopen(strcat('Results\',Object3,'.txt'),'w');
fprintf(file3,'Tracker Experiment Results ') ;
fprintf(file3, [date '\r\n']);
fprintf(file3, [Object3 '\r\n']);
fprintf(file3, '\t Translation \t\t\t Local Quaternion \t\t\t\t Local EulerXYZ \t\t\t\r\n ');
fprintf(file3,'%s\t %s\t %s\t %s\t %s\t %s\t %s\t %s\t %s\t %s\t %s\t\r\n','t','x','y','z','x','y','z','w','x','y','z');

file4 = fopen(strcat('Results\',Object4,'.txt'),'w');
fprintf(file4,'Tracker Experiment Results ') ;
fprintf(file4, [date '\r\n']);
fprintf(file4, [Object4 '\r\n']);
fprintf(file4, '\t Translation \t\t\t Local Quaternion \t\t\t\t Local EulerXYZ \t\t\t\r\n ');
fprintf(file4,'%s\t %s\t %s\t %s\t %s\t %s\t %s\t %s\t %s\t %s\t %s\t\r\n','t','x','y','z','x','y','z','w','x','y','z');

file5 = fopen(strcat('Results\',Object5,'.txt'),'w');
fprintf(file5,'Tracker Experiment Results ') ;
fprintf(file5, [date '\r\n']);
fprintf(file5, [Object5 '\r\n']);
fprintf(file5, '\t Translation \t\t\t Local Quaternion \t\t\t\t Local EulerXYZ \t\t\t\r\n ');
fprintf(file5,'%s\t %s\t %s\t %s\t %s\t %s\t %s\t %s\t %s\t %s\t %s\t\r\n','t','x','y','z','x','y','z','w','x','y','z');

file6 = fopen(strcat('Results\',Object6,'.txt'),'w');
fprintf(file6,'Tracker Experiment Results ') ;
fprintf(file6, [date '\r\n']);
fprintf(file6, [Object6 '\r\n']);
fprintf(file6, '\t Translation \t\t\t Local Quaternion \t\t\t\t Local EulerXYZ \t\t\t\r\n ');
fprintf(file6,'%s\t %s\t %s\t %s\t %s\t %s\t %s\t %s\t %s\t %s\t %s\t\r\n','t','x','y','z','x','y','z','w','x','y','z');

file7 = fopen(strcat('Results\',Object7,'.txt'),'w');
fprintf(file7,'Tracker Experiment Results ') ;
fprintf(file7, [date '\r\n']);
fprintf(file7, [Object7 '\r\n']);
fprintf(file7, '\t Translation \t\t\t Local Quaternion \t\t\t\t Local EulerXYZ \t\t\t\r\n ');
fprintf(file7,'%s\t %s\t %s\t %s\t %s\t %s\t %s\t %s\t %s\t %s\t %s\t\r\n','t','x','y','z','x','y','z','w','x','y','z');

file_sync = fopen(strcat('Results\','Synchro.txt'),'w');

index = 0;
% Loop until the message box is dismissed
while ishandle( MessageBox )
    drawnow;
    
    % Get a frame
    while MyClient.GetFrame().Result.Value ~= Result.Success
        fprintf( '.' );
    end% while
    
    Output_GetFrameNumber = MyClient.GetFrameNumber().FrameNumber;
    fprintf( 'Frame Number: %d\n', Output_GetFrameNumber);
    if index==0, initFrame = Output_GetFrameNumber; end
    
    time = (double(Output_GetFrameNumber) - double(initFrame))*0.01;

    %%%%%%%%%%%%%%%%%%%% Object 1 %%%%%%%%%%%%%%%%%
    % Get the global segment translation in helical co-ordinates
    translation1 = MyClient.GetSegmentGlobalTranslation(Object1,Object1).Translation;
     
    % Get the global segment rotation quaternion
    quaternion1 = MyClient.GetSegmentLocalRotationQuaternion(Object1,Object1);
    
    % Get the local segment rotation angles EULER XYZ
    euler1XYZ = MyClient.GetSegmentLocalRotationEulerXYZ(Object1,Object1);
   
    % Print into the result file
    if translation1 ~= 0, % if the object has been successfully tracked
    fprintf(file1, [num2str(time) '\t' num2str(translation1(1)) '\t' num2str(translation1(2)) '\t' num2str(translation1(3)) '\t']);
    fprintf(file1,'%.4f \t %.4f \t %.4f \t %.4f \t', quaternion1.Rotation);
    fprintf(file1,'%.4f \t %.4f \t %.4f \t \r\n', euler1XYZ.Rotation);
    end
    
     %%%%%%%%%%%%%%%%%%%% Object 2 %%%%%%%%%%%%%%%%%
    % Get the global segment translation in helical co-ordinates
    translation2 = MyClient.GetSegmentGlobalTranslation(Object2,Object2).Translation;
     
    % Get the global segment rotation quaternion
    quaternion2 = MyClient.GetSegmentLocalRotationQuaternion(Object2,Object2);
    
    % Get the local segment rotation angles EULER XYZ
    euler2XYZ = MyClient.GetSegmentLocalRotationEulerXYZ(Object2,Object2);
   
    % Print into the result file
    if translation2 ~= 0, % if the object has been successfully tracked
    fprintf(file2, [num2str(time) '\t' num2str(translation2(1)) '\t' num2str(translation2(2)) '\t' num2str(translation2(3)) '\t']);
    fprintf(file2,'%.4f \t %.4f \t %.4f \t %.4f \t', quaternion2.Rotation);
    fprintf(file2,'%.4f \t %.4f \t %.4f \t \r\n', euler2XYZ.Rotation);
    end
    
     %%%%%%%%%%%%%%%%%%%% Object 3 %%%%%%%%%%%%%%%%%
    % Get the global segment translation in helical co-ordinates
    translation3 = MyClient.GetSegmentGlobalTranslation(Object3,Object3).Translation;
     
    % Get the global segment rotation quaternion
    quaternion3 = MyClient.GetSegmentLocalRotationQuaternion(Object3,Object3);
    
    % Get the local segment rotation angles EULER XYZ
    euler3XYZ = MyClient.GetSegmentLocalRotationEulerXYZ(Object3,Object3);
   
    % Print into the result file
    if translation3 ~= 0, % if the object has been successfully tracked
    fprintf(file3, [num2str(time) '\t' num2str(translation3(1)) '\t' num2str(translation3(2)) '\t' num2str(translation3(3)) '\t']);
    fprintf(file3,'%.4f \t %.4f \t %.4f \t %.4f \t', quaternion3.Rotation);
    fprintf(file3,'%.4f \t %.4f \t %.4f \t \r\n', euler3XYZ.Rotation);
    end
   
    %%%%%%%%%%%%%%%%%%%% Object 4 %%%%%%%%%%%%%%%%%
    % Get the global segment translation in helical co-ordinates
    translation4 = MyClient.GetSegmentGlobalTranslation(Object4,Object4).Translation;
     
    % Get the global segment rotation quaternion
    quaternion4 = MyClient.GetSegmentLocalRotationQuaternion(Object4,Object4);
    
    % Get the local segment rotation angles EULER XYZ
    euler4XYZ = MyClient.GetSegmentLocalRotationEulerXYZ(Object4,Object4);
   
    % Print into the result file
    if translation4 ~= 0, % if the object has been successfully tracked
    fprintf(file4, [num2str(time) '\t' num2str(translation4(1)) '\t' num2str(translation4(2)) '\t' num2str(translation4(3)) '\t']);
    fprintf(file4,'%.4f \t %.4f \t %.4f \t %.4f \t', quaternion4.Rotation);
    fprintf(file4,'%.4f \t %.4f \t %.4f \t \r\n', euler4XYZ.Rotation);
    end
    
    %%%%%%%%%%%%%%%%%%%% Object 5 %%%%%%%%%%%%%%%%%
    % Get the global segment translation in helical co-ordinates
    translation5 = MyClient.GetSegmentGlobalTranslation(Object5,Object5).Translation;
     
    % Get the global segment rotation quaternion
    quaternion5 = MyClient.GetSegmentLocalRotationQuaternion(Object5,Object5);
    
    % Get the local segment rotation angles EULER XYZ
    euler5XYZ = MyClient.GetSegmentLocalRotationEulerXYZ(Object5,Object5);
   
    % Print into the result file
    if translation5 ~= 0, % if the object has been successfully tracked
    fprintf(file5, [num2str(time) '\t' num2str(translation5(1)) '\t' num2str(translation5(2)) '\t' num2str(translation5(3)) '\t']);
    fprintf(file5,'%.4f \t %.4f \t %.4f \t %.4f \t', quaternion5.Rotation);
    fprintf(file5,'%.4f \t %.4f \t %.4f \t \r\n', euler5XYZ.Rotation);
    end
    
    %%%%%%%%%%%%%%%%%%%% Object 6 %%%%%%%%%%%%%%%%%
    % Get the global segment translation in helical co-ordinates
    translation6 = MyClient.GetSegmentGlobalTranslation(Object6,Object6).Translation;
     
    % Get the global segment rotation quaternion
    quaternion6 = MyClient.GetSegmentLocalRotationQuaternion(Object6,Object6);
    
    % Get the local segment rotation angles EULER XYZ
    euler6XYZ = MyClient.GetSegmentLocalRotationEulerXYZ(Object6,Object6);
   
    % Print into the result file
    if translation6 ~= 0, % if the object has been successfully tracked
    fprintf(file6, [num2str(time) '\t' num2str(translation6(1)) '\t' num2str(translation6(2)) '\t' num2str(translation6(3)) '\t']);
    fprintf(file6,'%.4f \t %.4f \t %.4f \t %.4f \t', quaternion6.Rotation);
    fprintf(file6,'%.4f \t %.4f \t %.4f \t \r\n', euler6XYZ.Rotation);
    end
    
    %%%%%%%%%%%%%%%%%%%% Object 7 %%%%%%%%%%%%%%%%%
    % Get the global segment translation in helical co-ordinates
    translation7 = MyClient.GetSegmentGlobalTranslation(Object7,Object7).Translation;
     
    % Get the global segment rotation quaternion
    quaternion7 = MyClient.GetSegmentLocalRotationQuaternion(Object7,Object7);
    
    % Get the local segment rotation angles EULER XYZ
    euler7XYZ = MyClient.GetSegmentLocalRotationEulerXYZ(Object7,Object7);
   
    % Print into the result file
    if translation7 ~= 0, % if the object has been successfully tracked
    fprintf(file7, [num2str(time) '\t' num2str(translation7(1)) '\t' num2str(translation7(2)) '\t' num2str(translation7(3)) '\t']);
    fprintf(file7,'%.4f \t %.4f \t %.4f \t %.4f \t', quaternion7.Rotation);
    fprintf(file7,'%.4f \t %.4f \t %.4f \t \r\n', euler7XYZ.Rotation);
    end
    
    %Print sync value
    data_sync = session.inputSingleScan();
    fprintf(file_sync, [num2str(time) '\t' num2str(data_sync) '\n']);
    
    index=1;
end% while true
fclose(file1);
fclose(file2);
fclose(file3);
fclose(file4);
fclose(file5);
fclose(file6);
fclose(file7);

% Disconnect and dispose
MyClient.Disconnect();

% A dialog to visualize the results
ButtonName = questdlg('Do you want to visualize the results?', ...
    'Question');
switch ButtonName,
    case 'Yes',
        VisuResults7IMUs
    case 'No',
        close all
end

% Unload the SDK
fprintf( 'Unloading SDK...' );
Client.UnloadViconDataStreamSDK();
fprintf( 'done\n' );