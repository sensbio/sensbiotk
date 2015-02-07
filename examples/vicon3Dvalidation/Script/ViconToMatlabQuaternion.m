
% Load the SDK
fprintf( 'Loading SDK...' );
Client.LoadViconDataStreamSDK();
fprintf( 'done\n' );

% Program options
HostName = 'localhost:801';

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

% Set the streaming mode
MyClient.SetStreamMode( StreamMode.ClientPull );

MyClient.SetAxisMapping( Direction.Forward, ...
                         Direction.Left,    ...
                         Direction.Up );    % Z-up
%MyClient.SetAxisMapping( Direction.Forward, ...
%                         Direction.Up,      ...
%                         Direction.Right ); % Y-up

  
% A dialog to stop the loop
MessageBox = msgbox( 'Stop DataStream Client', version );
 
%Saved file
fileGlobalQuat = fopen('GLOBAL QUATERNION.txt','w');
fprintf(fileGlobalQuat,'GLOBAL QUATERNION\r\n');
fprintf(fileGlobalQuat,'%s\t %s\t %s\t %s\t %s\t\r\n','t','x','y','z','w');

fileLocalQuat = fopen('LOCAL QUATERNION.txt','w');
fprintf(fileLocalQuat,'LOCAL QUATERNION\r\n');
fprintf(fileLocalQuat,'%s\t %s\t %s\t %s\t %s\t\r\n','t','x','y','z','w');

fileGlobalEuler = fopen('GLOBAL EULER XYZ.txt','w');
fprintf(fileGlobalEuler,'GLOBAL EULER XYZ\r\n');
fprintf(fileGlobalEuler,'%s\t %s\t %s\t %s\t\r\n','t','x','y','z');

fileLocalEuler = fopen('LOCAL EULER XYZ.txt','w');
fprintf(fileLocalEuler,'LOCAL EULER XYZ\r\n');
fprintf(fileLocalEuler,'%s\t %s\t %s\t %s\t\r\n','t','x','y','z');

time = 0;
% Loop until the message box is dismissed
while ishandle( MessageBox )
 
  drawnow;
    
  % Get a frame
  while MyClient.GetFrame().Result.Value ~= Result.Success
    fprintf( '.' );
  end% while

  % Get the frame number
  Output_GetFrameNumber = MyClient.GetFrameNumber();
   fprintf( 'Frame Number: %d\n', Output_GetFrameNumber.FrameNumber );

  % Count the number of subjects
    
  % Get the subject name
  SubjectName = MyClient.GetSubjectName( 1 ).SubjectName;
    
  % Get the root segment
  RootSegment = MyClient.GetSubjectRootSegmentName( SubjectName ).SegmentName;

  
  % Get the global segment rotation in helical co-ordinates
  Output_GetSegmentGlobalRotationHelical = MyClient.GetSegmentGlobalRotationHelical( SubjectName, RootSegment );
%   fprintf( ' Global Rotation (Helical):\n  X : %g\n  Y : %g\n  Z : %g\n\n',             ...
%                      Output_GetSegmentGlobalRotationHelical.Rotation( 1 ), ...
%                      Output_GetSegmentGlobalRotationHelical.Rotation( 2 ), ...
%                      Output_GetSegmentGlobalRotationHelical.Rotation( 3 ) );
    
  % Get the global segment rotation quaternion
  Output_GetSegmentGlobalRotationQuaternion = MyClient.GetSegmentGlobalRotationQuaternion(SubjectName,RootSegment);
  fprintf(fileGlobalQuat,'%.3f \t %.4f \t %.4f \t %.4f \t %.4f \t \r\n',time, Output_GetSegmentGlobalRotationQuaternion.Rotation);

  % Get the local segment rotation quaternion
  Output_GetSegmentLocalRotationQuaternion = MyClient.GetSegmentLocalRotationQuaternion(SubjectName,RootSegment);
  fprintf(fileLocalQuat,'%.3f \t %.4f \t %.4f \t %.4f \t %.4f \t \r\n',time, Output_GetSegmentLocalRotationQuaternion.Rotation);

   % Get the global segment rotation angles EULER XYZ
  Output_GetSegmentGlobalRotationEulerXYZ = MyClient.GetSegmentGlobalRotationEulerXYZ(SubjectName,RootSegment);
  fprintf(fileGlobalEuler,'%.3f \t %.4f \t %.4f \t %.4f \t \r\n',time, Output_GetSegmentGlobalRotationEulerXYZ.Rotation);

  % Get the local segment rotation angles EULER XYZ
  Output_GetSegmentLocalRotationEulerXYZ = MyClient.GetSegmentLocalRotationEulerXYZ(SubjectName,RootSegment);
  fprintf(fileLocalEuler,'%.3f \t %.4f \t %.4f \t %.4f \t \r\n',time, Output_GetSegmentLocalRotationEulerXYZ.Rotation);

  time = time + 0.01;
  
end% while true  
fclose(fileGlobalQuat);
fclose(fileLocalQuat);
fclose(fileGlobalEuler);
fclose(fileLocalEuler);

% Disconnect and dispose
MyClient.Disconnect();

% Unload the SDK
fprintf( 'Unloading SDK...' );
Client.UnloadViconDataStreamSDK();
fprintf( 'done\n' );