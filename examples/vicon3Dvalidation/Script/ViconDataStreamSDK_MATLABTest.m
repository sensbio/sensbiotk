% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
% Copyright (C) OMG Plc 2009.
% All rights reserved.  This software is protected by copyright
% law and international treaties.  No part of this software / document
% may be reproduced or distributed in any form or by any means,
% whether transiently or incidentally to some other use of this software,
% without the written permission of the copyright owner.
%
% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Part of the Vicon DataStream SDK for MATLAB.
% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Program options
TransmitMulticast = false;

% A dialog to stop the loop
MessageBox = msgbox( 'Stop DataStream Client', 'Vicon DataStream SDK' );

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
  
  % Multicast connection
  % MyClient.ConnectToMulticast( HostName, '224.0.0.0' );
  
  fprintf( '.' );
end
fprintf( '\n' );

% Enable some different data types
MyClient.EnableSegmentData();
MyClient.EnableMarkerData();
MyClient.EnableUnlabeledMarkerData();
MyClient.EnableDeviceData();

fprintf( 'Segment Data Enabled: %s\n',          AdaptBool( MyClient.IsSegmentDataEnabled().Enabled ) );
fprintf( 'Marker Data Enabled: %s\n',           AdaptBool( MyClient.IsMarkerDataEnabled().Enabled ) );
fprintf( 'Unlabeled Marker Data Enabled: %s\n', AdaptBool( MyClient.IsUnlabeledMarkerDataEnabled().Enabled ) );
fprintf( 'Device Data Enabled: %s\n',           AdaptBool( MyClient.IsDeviceDataEnabled().Enabled ) );

% Set the streaming mode
MyClient.SetStreamMode( StreamMode.ClientPull );
% MyClient.SetStreamMode( StreamMode.ClientPullPreFetch );
% MyClient.SetStreamMode( StreamMode.ServerPush );

% Set the global up axis
MyClient.SetAxisMapping( Direction.Forward, ...
                         Direction.Left,    ...
                         Direction.Up );    % Z-up
% MyClient.SetAxisMapping( Direction.Forward, ...
%                          Direction.Up,      ...
%                          Direction.Right ); % Y-up

Output_GetAxisMapping = MyClient.GetAxisMapping();
fprintf( 'Axis Mapping: X-%s Y-%s Z-%s\n', Output_GetAxisMapping.XAxis.ToString(), ...
                                           Output_GetAxisMapping.YAxis.ToString(), ...
                                           Output_GetAxisMapping.ZAxis.ToString() );


% Discover the version number
Output_GetVersion = MyClient.GetVersion();
fprintf( 'Version: %d.%d.%d\n', Output_GetVersion.Major, ...
                                Output_GetVersion.Minor, ...
                                Output_GetVersion.Point );
  
if TransmitMulticast
  MyClient.StartTransmittingMulticast( 'localhost', '224.0.0.0' );
end  
  
% Loop until the message box is dismissed
while ishandle( MessageBox )
  drawnow;
    
  % Get a frame
  fprintf( 'Waiting for new frame...' );
  while MyClient.GetFrame().Result.Value ~= Result.Success
    fprintf( '.' );
  end% while
  fprintf( '\n' );  

  % Get the frame number
  Output_GetFrameNumber = MyClient.GetFrameNumber();
  fprintf( 'Frame Number: %d\n', Output_GetFrameNumber.FrameNumber );

  % Get the frame rate
  Output_GetFrameRate = MyClient.GetFrameRate();
  fprintf( 'Frame rate: %g\n', Output_GetFrameRate.FrameRateHz );

  % Get the timecode
  Output_GetTimecode = MyClient.GetTimecode();
  fprintf( 'Timecode: %dh %dm %ds %df %dsf %s %d %d %d\n\n',    ...
                     Output_GetTimecode.Hours,                  ...
                     Output_GetTimecode.Minutes,                ...
                     Output_GetTimecode.Seconds,                ...
                     Output_GetTimecode.Frames,                 ...
                     Output_GetTimecode.SubFrame,               ...
                     AdaptBool( Output_GetTimecode.FieldFlag ), ...
                     Output_GetTimecode.Standard.Value,         ...
                     Output_GetTimecode.SubFramesPerFrame,      ...
                     Output_GetTimecode.UserBits );

  % Get the latency
  fprintf( 'Latency: %gs\n', MyClient.GetLatencyTotal().Total );
  
  for LatencySampleIndex = 1:MyClient.GetLatencySampleCount().Count
    SampleName  = MyClient.GetLatencySampleName( LatencySampleIndex ).Name;
    SampleValue = MyClient.GetLatencySampleValue( SampleName ).Value;

    fprintf( '  %s %gs\n', SampleName, SampleValue );
  end% for  
  fprintf( '\n' );
                     
  % Count the number of subjects
  SubjectCount = MyClient.GetSubjectCount().SubjectCount;
  fprintf( 'Subjects (%d):\n', SubjectCount );
  for SubjectIndex = 1:SubjectCount
    fprintf( '  Subject #%d\n', SubjectIndex - 1 );
    
    % Get the subject name
    SubjectName = MyClient.GetSubjectName( SubjectIndex ).SubjectName;
    fprintf( '    Name: %s\n', SubjectName );
    
    % Get the root segment
    RootSegment = MyClient.GetSubjectRootSegmentName( SubjectName ).SegmentName;
    fprintf( '    Root Segment: %s\n', RootSegment );

    % Count the number of segments
    SegmentCount = MyClient.GetSegmentCount( SubjectName ).SegmentCount;
    fprintf( '    Segments (%d):\n', SegmentCount );
    for SegmentIndex = 1:SegmentCount
      fprintf( '      Segment #%d\n', SegmentIndex - 1 );
      
      % Get the segment name
      SegmentName = MyClient.GetSegmentName( SubjectName, SegmentIndex ).SegmentName;
      fprintf( '        Name: %s\n', SegmentName );
      
      % Get the segment parent
      SegmentParentName = MyClient.GetSegmentParentName( SubjectName, SegmentName ).SegmentName;
      fprintf( '        Parent: %s\n',  SegmentParentName );

      % Get the segment's children
      ChildCount = MyClient.GetSegmentChildCount( SubjectName, SegmentName ).SegmentCount;
      fprintf( '     Children (%d):\n', ChildCount );
      for ChildIndex = 1:ChildCount
        ChildName = MyClient.GetSegmentChildName( SubjectName, SegmentName, ChildIndex ).SegmentName;
        fprintf( '       %s\n', ChildName );
      end% for  

      % Get the static segment translation
      Output_GetSegmentStaticTranslation = MyClient.GetSegmentStaticTranslation( SubjectName, SegmentName );
      fprintf( '        Static Translation: (%g, %g, %g)\n',                  ...
                         Output_GetSegmentStaticTranslation.Translation( 1 ), ...
                         Output_GetSegmentStaticTranslation.Translation( 2 ), ...
                         Output_GetSegmentStaticTranslation.Translation( 3 ) );
      
      % Get the static segment rotation in helical co-ordinates
      Output_GetSegmentStaticRotationHelical = MyClient.GetSegmentStaticRotationHelical( SubjectName, SegmentName );
      fprintf( '        Static Rotation Helical: (%g, %g, %g)\n',              ...
                         Output_GetSegmentStaticRotationHelical.Rotation( 1 ), ...
                         Output_GetSegmentStaticRotationHelical.Rotation( 2 ), ...
                         Output_GetSegmentStaticRotationHelical.Rotation( 3 ) );
      
      % Get the static segment rotation as a matrix
      Output_GetSegmentStaticRotationMatrix = MyClient.GetSegmentStaticRotationMatrix( SubjectName, SegmentName );
      fprintf( '        Static Rotation Matrix: (%g, %g, %g, %g, %g, %g, %g, %g, %g)\n', ...
                         Output_GetSegmentStaticRotationMatrix.Rotation( 1 ),            ...
                         Output_GetSegmentStaticRotationMatrix.Rotation( 2 ),            ...
                         Output_GetSegmentStaticRotationMatrix.Rotation( 3 ),            ...
                         Output_GetSegmentStaticRotationMatrix.Rotation( 4 ),            ...
                         Output_GetSegmentStaticRotationMatrix.Rotation( 5 ),            ...
                         Output_GetSegmentStaticRotationMatrix.Rotation( 6 ),            ...
                         Output_GetSegmentStaticRotationMatrix.Rotation( 7 ),            ...
                         Output_GetSegmentStaticRotationMatrix.Rotation( 8 ),            ...
                         Output_GetSegmentStaticRotationMatrix.Rotation( 9 ) );
      
      % Get the static segment rotation in quaternion co-ordinates
      Output_GetSegmentStaticRotationQuaternion = MyClient.GetSegmentStaticRotationQuaternion( SubjectName, SegmentName );
      fprintf( '        Static Rotation Quaternion: (%g, %g, %g, %g)\n',          ...
                         Output_GetSegmentStaticRotationQuaternion.Rotation( 1 ), ...
                         Output_GetSegmentStaticRotationQuaternion.Rotation( 2 ), ...
                         Output_GetSegmentStaticRotationQuaternion.Rotation( 3 ), ...
                         Output_GetSegmentStaticRotationQuaternion.Rotation( 4 ) );

      % Get the static segment rotation in EulerXYZ co-ordinates
      Output_GetSegmentStaticRotationEulerXYZ = MyClient.GetSegmentStaticRotationEulerXYZ( SubjectName, SegmentName );
      fprintf( '        Static Rotation EulerXYZ: (%g, %g, %g)\n',               ...
                         Output_GetSegmentStaticRotationEulerXYZ.Rotation( 1 ),  ...
                         Output_GetSegmentStaticRotationEulerXYZ.Rotation( 2 ),  ...
                         Output_GetSegmentStaticRotationEulerXYZ.Rotation( 3 ) );

      % Get the global segment translation
      Output_GetSegmentGlobalTranslation = MyClient.GetSegmentGlobalTranslation( SubjectName, SegmentName );
      fprintf( '        Global Translation: (%g, %g, %g) %s\n',               ...
                         Output_GetSegmentGlobalTranslation.Translation( 1 ), ...
                         Output_GetSegmentGlobalTranslation.Translation( 2 ), ...
                         Output_GetSegmentGlobalTranslation.Translation( 3 ), ...
                         AdaptBool( Output_GetSegmentGlobalTranslation.Occluded ) );
      
      % Get the global segment rotation in helical co-ordinates
      Output_GetSegmentGlobalRotationHelical = MyClient.GetSegmentGlobalRotationHelical( SubjectName, SegmentName );
      fprintf( '        Global Rotation Helical: (%g, %g, %g) %s\n',           ...
                         Output_GetSegmentGlobalRotationHelical.Rotation( 1 ), ...
                         Output_GetSegmentGlobalRotationHelical.Rotation( 2 ), ...
                         Output_GetSegmentGlobalRotationHelical.Rotation( 3 ), ...
                         AdaptBool( Output_GetSegmentGlobalRotationHelical.Occluded ) );
      
      % Get the global segment rotation as a matrix
      Output_GetSegmentGlobalRotationMatrix = MyClient.GetSegmentGlobalRotationMatrix( SubjectName, SegmentName );
      fprintf( '        Global Rotation Matrix: (%g, %g, %g, %g, %g, %g, %g, %g, %g) %s\n', ...
                         Output_GetSegmentGlobalRotationMatrix.Rotation( 1 ),               ...
                         Output_GetSegmentGlobalRotationMatrix.Rotation( 2 ),               ...
                         Output_GetSegmentGlobalRotationMatrix.Rotation( 3 ),               ...
                         Output_GetSegmentGlobalRotationMatrix.Rotation( 4 ),               ...
                         Output_GetSegmentGlobalRotationMatrix.Rotation( 5 ),               ...
                         Output_GetSegmentGlobalRotationMatrix.Rotation( 6 ),               ...
                         Output_GetSegmentGlobalRotationMatrix.Rotation( 7 ),               ...
                         Output_GetSegmentGlobalRotationMatrix.Rotation( 8 ),               ...
                         Output_GetSegmentGlobalRotationMatrix.Rotation( 9 ),               ...
                         AdaptBool( Output_GetSegmentGlobalRotationMatrix.Occluded ) );
      
      % Get the global segment rotation in quaternion co-ordinates
      Output_GetSegmentGlobalRotationQuaternion = MyClient.GetSegmentGlobalRotationQuaternion( SubjectName, SegmentName );
      fprintf( '        Global Rotation Quaternion: (%g, %g, %g, %g) %s\n',             ...
                         Output_GetSegmentGlobalRotationQuaternion.Rotation( 1 ),       ...
                         Output_GetSegmentGlobalRotationQuaternion.Rotation( 2 ),       ...
                         Output_GetSegmentGlobalRotationQuaternion.Rotation( 3 ),       ...
                         Output_GetSegmentGlobalRotationQuaternion.Rotation( 4 ),       ...
                         AdaptBool( Output_GetSegmentGlobalRotationQuaternion.Occluded ) );

      % Get the global segment rotation in EulerXYZ co-ordinates
      Output_GetSegmentGlobalRotationEulerXYZ = MyClient.GetSegmentGlobalRotationEulerXYZ( SubjectName, SegmentName );
      fprintf( '        Global Rotation EulerXYZ: (%g, %g, %g) %s\n',                 ...
                         Output_GetSegmentGlobalRotationEulerXYZ.Rotation( 1 ),       ...
                         Output_GetSegmentGlobalRotationEulerXYZ.Rotation( 2 ),       ...
                         Output_GetSegmentGlobalRotationEulerXYZ.Rotation( 3 ),       ...
                         AdaptBool( Output_GetSegmentGlobalRotationEulerXYZ.Occluded ) );

      % Get the local segment translation
      Output_GetSegmentLocalTranslation = MyClient.GetSegmentLocalTranslation( SubjectName, SegmentName );
      fprintf( '        Local Translation: (%g, %g, %g) %s\n',               ...
                         Output_GetSegmentLocalTranslation.Translation( 1 ), ...
                         Output_GetSegmentLocalTranslation.Translation( 2 ), ...
                         Output_GetSegmentLocalTranslation.Translation( 3 ), ...
                         AdaptBool( Output_GetSegmentLocalTranslation.Occluded ) );
      
      % Get the local segment rotation in helical co-ordinates
      Output_GetSegmentLocalRotationHelical = MyClient.GetSegmentLocalRotationHelical( SubjectName, SegmentName );
      fprintf( '        Local Rotation Helical: (%g, %g, %g) %s\n',           ...
                         Output_GetSegmentLocalRotationHelical.Rotation( 1 ), ...
                         Output_GetSegmentLocalRotationHelical.Rotation( 2 ), ...
                         Output_GetSegmentLocalRotationHelical.Rotation( 3 ), ...
                         AdaptBool( Output_GetSegmentLocalRotationHelical.Occluded ) );
      
      % Get the local segment rotation as a matrix
      Output_GetSegmentLocalRotationMatrix = MyClient.GetSegmentLocalRotationMatrix( SubjectName, SegmentName );
      fprintf( '        Local Rotation Matrix: (%g, %g, %g, %g, %g, %g, %g, %g, %g) %s\n', ...
                         Output_GetSegmentLocalRotationMatrix.Rotation( 1 ),               ...
                         Output_GetSegmentLocalRotationMatrix.Rotation( 2 ),               ...
                         Output_GetSegmentLocalRotationMatrix.Rotation( 3 ),               ...
                         Output_GetSegmentLocalRotationMatrix.Rotation( 4 ),               ...
                         Output_GetSegmentLocalRotationMatrix.Rotation( 5 ),               ...
                         Output_GetSegmentLocalRotationMatrix.Rotation( 6 ),               ...
                         Output_GetSegmentLocalRotationMatrix.Rotation( 7 ),               ...
                         Output_GetSegmentLocalRotationMatrix.Rotation( 8 ),               ...
                         Output_GetSegmentLocalRotationMatrix.Rotation( 9 ),               ...
                         AdaptBool( Output_GetSegmentLocalRotationMatrix.Occluded ) );
      
      % Get the local segment rotation in quaternion co-ordinates
      Output_GetSegmentLocalRotationQuaternion = MyClient.GetSegmentLocalRotationQuaternion( SubjectName, SegmentName );
      fprintf( '        Local Rotation Quaternion: (%g, %g, %g, %g) %s\n',             ...
                         Output_GetSegmentLocalRotationQuaternion.Rotation( 1 ),       ...
                         Output_GetSegmentLocalRotationQuaternion.Rotation( 2 ),       ...
                         Output_GetSegmentLocalRotationQuaternion.Rotation( 3 ),       ...
                         Output_GetSegmentLocalRotationQuaternion.Rotation( 4 ),       ...
                         AdaptBool( Output_GetSegmentLocalRotationQuaternion.Occluded ) );

      % Get the local segment rotation in EulerXYZ co-ordinates
      Output_GetSegmentLocalRotationEulerXYZ = MyClient.GetSegmentLocalRotationEulerXYZ( SubjectName, SegmentName );
      fprintf( '        Local Rotation EulerXYZ: (%g, %g, %g) %s\n',                 ...
                         Output_GetSegmentLocalRotationEulerXYZ.Rotation( 1 ),       ...
                         Output_GetSegmentLocalRotationEulerXYZ.Rotation( 2 ),       ...
                         Output_GetSegmentLocalRotationEulerXYZ.Rotation( 3 ),       ...
                         AdaptBool( Output_GetSegmentLocalRotationEulerXYZ.Occluded ) );

    end% SegmentIndex
    
    % Count the number of markers
    MarkerCount = MyClient.GetMarkerCount( SubjectName ).MarkerCount;
    fprintf( '    Markers (%d):\n', MarkerCount );
    for MarkerIndex = 1:MarkerCount
      % Get the marker name
      MarkerName = MyClient.GetMarkerName( SubjectName, MarkerIndex ).MarkerName;

      % Get the marker parent
      MarkerParentName = MyClient.GetMarkerParentName( SubjectName, MarkerName ).SegmentName;

      % Get the global marker translation
      Output_GetMarkerGlobalTranslation = MyClient.GetMarkerGlobalTranslation( SubjectName, MarkerName );

      fprintf( '      Marker #%d: %s (%g, %g, %g) %s\n',                     ...
                         MarkerIndex - 1,                                    ...
                         MarkerName,                                         ...
                         Output_GetMarkerGlobalTranslation.Translation( 1 ), ...
                         Output_GetMarkerGlobalTranslation.Translation( 2 ), ...
                         Output_GetMarkerGlobalTranslation.Translation( 3 ), ...
                         AdaptBool( Output_GetMarkerGlobalTranslation.Occluded ) );
    end% MarkerIndex
    
  end% SubjectIndex

  % Get the unlabeled markers
  UnlabeledMarkerCount = MyClient.GetUnlabeledMarkerCount().MarkerCount;
  fprintf( '    Unlabeled Markers (%d):\n', UnlabeledMarkerCount );
  for UnlabeledMarkerIndex = 1:UnlabeledMarkerCount
    % Get the global marker translation
    Output_GetUnlabeledMarkerGlobalTranslation = MyClient.GetUnlabeledMarkerGlobalTranslation( UnlabeledMarkerIndex );
    fprintf( '      Marker #%d: (%g, %g, %g)\n',                                    ...
                       UnlabeledMarkerIndex - 1,                                    ...
                       Output_GetUnlabeledMarkerGlobalTranslation.Translation( 1 ), ...
                       Output_GetUnlabeledMarkerGlobalTranslation.Translation( 2 ), ...
                       Output_GetUnlabeledMarkerGlobalTranslation.Translation( 3 ) );
  end% UnlabeledMarkerIndex

  % Count the number of devices
  DeviceCount = MyClient.GetDeviceCount().DeviceCount;
  fprintf( '  Devices (%d):\n', DeviceCount );
  for DeviceIndex = 1:DeviceCount
    fprintf( '    Device #%d:\n', DeviceIndex - 1 );
    
    % Get the device name and type
    Output_GetDeviceName = MyClient.GetDeviceName( DeviceIndex );
    fprintf( '      Name: %s\n', Output_GetDeviceName.DeviceName );
    fprintf( '      Type: %s\n', Output_GetDeviceName.DeviceType.ToString() );
    
    
    % Count the number of device outputs
    DeviceOutputCount = MyClient.GetDeviceOutputCount( Output_GetDeviceName.DeviceName ).DeviceOutputCount;
    fprintf( '      Device Outputs (%d):\n', DeviceOutputCount );
    for DeviceOutputIndex = 1:DeviceOutputCount
      % Get the device output name and unit
      Output_GetDeviceOutputName = MyClient.GetDeviceOutputName( Output_GetDeviceName.DeviceName, DeviceOutputIndex );

      % Get the number of subsamples associated with this device.
      Output_GetDeviceOutputSubsamples = MyClient.GetDeviceOutputSubsamples( Output_GetDeviceName.DeviceName, Output_GetDeviceOutputName.DeviceOutputName );

      fprintf( '      Device Output #%d:\n', DeviceOutputIndex - 1 );

      fprintf( '      Samples (%d):\n', Output_GetDeviceOutputSubsamples.DeviceOutputSubsamples );


      for DeviceOutputSubsample = 1:Output_GetDeviceOutputSubsamples.DeviceOutputSubsamples
        fprintf( '        Sample #%d:\n', DeviceOutputSubsample - 1 );
        % Get the device output value
        Output_GetDeviceOutputValue = MyClient.GetDeviceOutputValue( Output_GetDeviceName.DeviceName, Output_GetDeviceOutputName.DeviceOutputName, DeviceOutputSubsample );

        fprintf( '          ''%s'' %g %s %s\n',                                    ...
                           Output_GetDeviceOutputName.DeviceOutputName,            ...
                           Output_GetDeviceOutputValue.Value,                      ...
                           Output_GetDeviceOutputName.DeviceOutputUnit.ToString(), ...
                           AdaptBool( Output_GetDeviceOutputValue.Occluded ) );
      end% DeviceOutputSubsample
    end% DeviceOutputIndex
    
  end% DeviceIndex
    
  % Count the number of force plates
  ForcePlateCount = MyClient.GetForcePlateCount().ForcePlateCount;
  fprintf( '  Force Plates: (%d)\n', ForcePlateCount );
  for ForcePlateIndex = 1:ForcePlateCount
    fprintf( '    Force Plate #%d:\n', ForcePlateIndex - 1 );
    
    % Get the number of subsamples associated with this device.
    Output_GetForcePlateSubsamples = MyClient.GetForcePlateSubsamples( ForcePlateIndex );
    
    fprintf( '    Samples (%d):\n', Output_GetForcePlateSubsamples.ForcePlateSubsamples );
    for ForcePlateSubsample = 1:Output_GetForcePlateSubsamples.ForcePlateSubsamples
      % Output all the subsamples.
      fprintf( '      Sample #%d:\n', ForcePlateSubsample - 1 );
      
      Output_GetGlobalForceVector = MyClient.GetGlobalForceVector( ForcePlateIndex, ForcePlateSubsample );
      fprintf( '      Force (%g, %g, %g)\n',                           ...
                         Output_GetGlobalForceVector.ForceVector( 1 ), ...
                         Output_GetGlobalForceVector.ForceVector( 2 ), ...
                         Output_GetGlobalForceVector.ForceVector( 3 ) );
    
      Output_GetGlobalMomentVector = MyClient.GetGlobalMomentVector( ForcePlateIndex, ForcePlateSubsample );
      fprintf( '      Moment (%g, %g, %g)\n',                            ...
                         Output_GetGlobalMomentVector.MomentVector( 1 ), ...
                         Output_GetGlobalMomentVector.MomentVector( 2 ), ...
                         Output_GetGlobalMomentVector.MomentVector( 3 ) );
    
      Output_GetGlobalCentreOfPressure = MyClient.GetGlobalCentreOfPressure( ForcePlateIndex, ForcePlateSubsample );
      fprintf( '      CoP (%g, %g, %g)\n',                                       ...
                         Output_GetGlobalCentreOfPressure.CentreOfPressure( 1 ), ...
                         Output_GetGlobalCentreOfPressure.CentreOfPressure( 2 ), ...
                         Output_GetGlobalCentreOfPressure.CentreOfPressure( 3 ) );    
    end% ForcePlateSubsample                     
  end% ForcePlateIndex
  
  % Count the number of eye trackers
  EyeTrackerCount = MyClient.GetEyeTrackerCount().EyeTrackerCount;
  fprintf( '  Eye Trackers: (%d)\n', EyeTrackerCount );
  for EyeTrackerIndex = 1:EyeTrackerCount
    fprintf( '    Eye Tracker #%d:\n', EyeTrackerIndex - 1 );

    Output_GetEyeTrackerGlobalPosition = MyClient.GetEyeTrackerGlobalPosition( EyeTrackerIndex );
    fprintf( '      Position (%g, %g, %g) %s\n',                       ...
                     Output_GetEyeTrackerGlobalPosition.Position( 1 ), ...
                     Output_GetEyeTrackerGlobalPosition.Position( 2 ), ...
                     Output_GetEyeTrackerGlobalPosition.Position( 3 ), ...
                     AdaptBool( Output_GetEyeTrackerGlobalPosition.Occluded ) );
   
    Output_GetEyeTrackerGlobalGazeVector = MyClient.GetEyeTrackerGlobalGazeVector( EyeTrackerIndex );
    fprintf( '      Gaze (%g, %g, %g) %s\n',                               ...
                     Output_GetEyeTrackerGlobalGazeVector.GazeVector( 1 ), ...
                     Output_GetEyeTrackerGlobalGazeVector.GazeVector( 2 ), ...
                     Output_GetEyeTrackerGlobalGazeVector.GazeVector( 3 ), ... 
                     AdaptBool( Output_GetEyeTrackerGlobalGazeVector.Occluded ) );
     
  end% EyeTrackerIndex  
    
end% while true  

if TransmitMulticast
  MyClient.StopTransmittingMulticast();
end  

% Disconnect and dispose
MyClient.Disconnect();

% Unload the SDK
fprintf( 'Unloading SDK...' );
Client.UnloadViconDataStreamSDK();
fprintf( 'done\n' );
