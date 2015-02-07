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
% Part of the ViconDataStream SDK for MATLAB.
% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
classdef Client
  properties % (SetAccess = private)
    InstanceID
  end

  methods(Static = true)
%% LoadViconDataStreamSDK
    function LoadViconDataStreamSDK()
      loadlibrary( 'ViconDataStreamSDK_MATLAB.dll' , 'ViconDataStreamSDK_MATLAB.h' )
    end
    
%% UnloadViconDataStreamSDK
    function UnloadViconDataStreamSDK()
      unloadlibrary  ViconDataStreamSDK_MATLAB
    end

  end% methods
  
  methods
%% Constructor      
    function obj = Client()
      obj.InstanceID = calllib( 'ViconDataStreamSDK_MATLAB', 'ConstructInstance_v2' );
    end% Constructor
    
%% Destructor
    function delete( obj )
      calllib( 'ViconDataStreamSDK_MATLAB', 'DestroyInstance_v2', obj.InstanceID ); 
    end
    
%% GetVersion
    function [Output] = GetVersion( obj )
      % Local data
      vMajor = 0;
      pMajor = libpointer( 'uint32Ptr', vMajor );

      vMinor = 0;
      pMinor = libpointer( 'uint32Ptr', vMinor );

      vPoint = 0;
      pPoint = libpointer( 'uint32Ptr', vPoint );

      % Call function
      calllib( 'ViconDataStreamSDK_MATLAB', 'GetVersion_v2', obj.InstanceID, pMajor, pMinor, pPoint );

      % Copy out data
      Major = get( pMajor, 'Value' );
      Minor = get( pMinor, 'Value' );
      Point = get( pPoint, 'Value' );
      
      Output = struct( 'Major', Major, 'Minor', Minor, 'Point', Point );
    end% GetVersion
    
%% Connect
    function [Output] = Connect( obj, HostName )
      % Local Data
      vResult = 0;
      pResult = libpointer( 'uint32Ptr', vResult );
      
      % Call function
      calllib( 'ViconDataStreamSDK_MATLAB', 'Connect_v2', obj.InstanceID, HostName, pResult );

      % Copy out data
      cResult = Result( get( pResult, 'Value' ) );
      
      Output = struct( 'Result', cResult );
    end

%% ConnectToMulticast
    function [Output] = ConnectToMulticast( obj, HostName, MulticastIP )
      % Local Data
      vResult = 0;
      pResult = libpointer( 'uint32Ptr', vResult );
      
      % Call function
      calllib( 'ViconDataStreamSDK_MATLAB', 'ConnectToMulticast_v2', obj.InstanceID, HostName, MulticastIP, pResult );

      % Copy out data
      cResult = Result( get( pResult, 'Value' ) );
      
      Output = struct( 'Result', cResult );
    end

%% Disconnect
    function [Output] = Disconnect( obj )
      % Local Data
      vResult = 0;
      pResult = libpointer( 'uint32Ptr', vResult );
      
      % Call function
      calllib( 'ViconDataStreamSDK_MATLAB', 'Disconnect_v2', obj.InstanceID, pResult );

      % Copy out data
      cResult = Result( get( pResult, 'Value' ) );
      
      Output = struct( 'Result', cResult );
      
    end

%% IsConnected
    function [Output] = IsConnected( obj )
      % Call function
      vConnected = calllib( 'ViconDataStreamSDK_MATLAB', 'IsConnected_v2', obj.InstanceID );

      % Copy out data
      Output = struct( 'Connected', vConnected );
      
    end

%% StartTransmittingMulticast
    function [Output] = StartTransmittingMulticast( obj, ServerIP, MulticastIP )
      % Local Data
      vResult = 0;
      pResult = libpointer( 'uint32Ptr', vResult );

      % Call function
      calllib( 'ViconDataStreamSDK_MATLAB', 'StartTransmittingMulticast_v2', obj.InstanceID, ServerIP, MulticastIP, pResult );

      % Copy out data
      cResult = Result( get( pResult, 'Value' ) );
      
      Output = struct( 'Result', cResult );
      
    end

%% StopTransmittingMulticast
    function [Output] = StopTransmittingMulticast( obj )
      % Local Data
      vResult = 0;
      pResult = libpointer( 'uint32Ptr', vResult );

      % Call function
      calllib( 'ViconDataStreamSDK_MATLAB', 'StopTransmittingMulticast_v2', obj.InstanceID, pResult );

      % Copy out data
      cResult = Result( get( pResult, 'Value' ) );
      
      Output = struct( 'Result', cResult );
      
    end

%% EnableSegmentData
    function [Output] = EnableSegmentData( obj )
      % Local Data
      vResult = 0;
      pResult = libpointer( 'uint32Ptr', vResult );

      % Call function
      vConnected = calllib( 'ViconDataStreamSDK_MATLAB', 'EnableSegmentData_v2', obj.InstanceID, pResult );

      % Copy out data
      cResult = Result( get( pResult, 'Value' ) );
      
      Output = struct( 'Result', cResult );
      
    end

%% EnableMarkerData
    function [Output] = EnableMarkerData( obj )
      % Local Data
      vResult = 0;
      pResult = libpointer( 'uint32Ptr', vResult );

      % Call function
      vConnected = calllib( 'ViconDataStreamSDK_MATLAB', 'EnableMarkerData_v2', obj.InstanceID, pResult );

      % Copy out data
      cResult = Result( get( pResult, 'Value' ) );
      
      Output = struct( 'Result', cResult );
      
    end

%% EnableUnlabeledMarkerData
    function [Output] = EnableUnlabeledMarkerData( obj )
      % Local Data
      vResult = 0;
      pResult = libpointer( 'uint32Ptr', vResult );

      % Call function
      vConnected = calllib( 'ViconDataStreamSDK_MATLAB', 'EnableUnlabeledMarkerData_v2', obj.InstanceID, pResult );

      % Copy out data
      cResult = Result( get( pResult, 'Value' ) );
      
      Output = struct( 'Result', cResult );
      
    end

%% EnableDeviceData
    function [Output] = EnableDeviceData( obj )
      % Local Data
      vResult = 0;
      pResult = libpointer( 'uint32Ptr', vResult );

      % Call function
      vConnected = calllib( 'ViconDataStreamSDK_MATLAB', 'EnableDeviceData_v2', obj.InstanceID, pResult );

      % Copy out data
      cResult = Result( get( pResult, 'Value' ) );
      
      Output = struct( 'Result', cResult );
      
    end

%% DisableSegmentData
    function [Output] = DisableSegmentData( obj )
      % Local Data
      vResult = 0;
      pResult = libpointer( 'uint32Ptr', vResult );

      % Call function
      vConnected = calllib( 'ViconDataStreamSDK_MATLAB', 'DisableSegmentData_v2', obj.InstanceID, pResult );

      % Copy out data
      cResult = Result( get( pResult, 'Value' ) );
      
      Output = struct( 'Result', cResult );
      
    end

%% DisableMarkerData
    function [Output] = DisableMarkerData( obj )
      % Local Data
      vResult = 0;
      pResult = libpointer( 'uint32Ptr', vResult );

      % Call function
      vConnected = calllib( 'ViconDataStreamSDK_MATLAB', 'DisableMarkerData_v2', obj.InstanceID, pResult );

      % Copy out data
      cResult = Result( get( pResult, 'Value' ) );
      
      Output = struct( 'Result', cResult );
      
    end

%% DisableUnlabeledMarkerData
    function [Output] = DisableUnlabeledMarkerData( obj )
      % Local Data
      vResult = 0;
      pResult = libpointer( 'uint32Ptr', vResult );

      % Call function
      vConnected = calllib( 'ViconDataStreamSDK_MATLAB', 'DisableUnlabeledMarkerData_v2', obj.InstanceID, pResult );

      % Copy out data
      cResult = Result( get( pResult, 'Value' ) );
      
      Output = struct( 'Result', cResult );
      
    end

%% DisableDeviceData
    function [Output] = DisableDeviceData( obj )
      % Local Data
      vResult = 0;
      pResult = libpointer( 'uint32Ptr', vResult );

      % Call function
      vConnected = calllib( 'ViconDataStreamSDK_MATLAB', 'DisableDeviceData_v2', obj.InstanceID, pResult );

      % Copy out data
      cResult = Result( get( pResult, 'Value' ) );
      
      Output = struct( 'Result', cResult );
      
    end

%% IsSegmentDataEnabled
    function [Output] = IsSegmentDataEnabled( obj )
      % Call function
      vEnabled = calllib( 'ViconDataStreamSDK_MATLAB', 'IsSegmentDataEnabled_v2', obj.InstanceID );

      % Copy out data
      Output = struct( 'Enabled', vEnabled );
      
    end

%% IsMarkerDataEnabled
    function [Output] = IsMarkerDataEnabled( obj )
      % Call function
      vEnabled = calllib( 'ViconDataStreamSDK_MATLAB', 'IsMarkerDataEnabled_v2', obj.InstanceID );

      % Copy out data
      Output = struct( 'Enabled', vEnabled );
      
    end

%% IsUnlabeledMarkerDataEnabled
    function [Output] = IsUnlabeledMarkerDataEnabled( obj )
      % Call function
      vEnabled = calllib( 'ViconDataStreamSDK_MATLAB', 'IsUnlabeledMarkerDataEnabled_v2', obj.InstanceID );

      % Copy out data
      Output = struct( 'Enabled', vEnabled );
      
    end

%% IsDeviceDataEnabled
    function [Output] = IsDeviceDataEnabled( obj )
      % Call function
      vEnabled = calllib( 'ViconDataStreamSDK_MATLAB', 'IsDeviceDataEnabled_v2', obj.InstanceID );

      % Copy out data
      Output = struct( 'Enabled', vEnabled );
      
    end

%% SetStreamMode
    function [Output] = SetStreamMode( obj, Mode )
      % Local Data
      vResult = 0;
      pResult = libpointer( 'uint32Ptr', vResult );

      % Call function
      calllib( 'ViconDataStreamSDK_MATLAB', 'SetStreamMode_v2', obj.InstanceID, Mode, pResult );

      % Copy out data
      cResult = Result( get( pResult, 'Value' ) );
      
      Output = struct( 'Result', cResult );
      
    end

%% SetAxisMapping
    function [Output] = SetAxisMapping( obj, XAxis, YAxis, ZAxis )
      % Local Data
      vResult = 0;
      pResult = libpointer( 'uint32Ptr', vResult );

      % Call function
      calllib( 'ViconDataStreamSDK_MATLAB', 'SetAxisMapping_v2', obj.InstanceID, XAxis, YAxis, ZAxis, pResult );

      % Copy out data
      cResult = Result( get( pResult, 'Value' ) );
      
      Output = struct( 'Result', cResult );
      
    end

%% GetAxisMapping
    function [Output] = GetAxisMapping( obj )
      % Local Data
      vXAxis = 0;
      pXAxis = libpointer( 'uint32Ptr', vXAxis );
      vYAxis = 0;
      pYAxis = libpointer( 'uint32Ptr', vYAxis );
      vZAxis = 0;
      pZAxis = libpointer( 'uint32Ptr', vZAxis );

      % Call function
      calllib( 'ViconDataStreamSDK_MATLAB', 'GetAxisMapping_v2', obj.InstanceID, pXAxis, pYAxis, pZAxis );

      % Copy out data
      cXAxis  = Direction( get( pXAxis,  'Value' ) );
      cYAxis  = Direction( get( pYAxis,  'Value' ) );
      cZAxis  = Direction( get( pZAxis,  'Value' ) );
      
      Output = struct( 'XAxis', cXAxis, 'YAxis', cYAxis, 'ZAxis', cZAxis );
      
    end

%% GetFrame
    function [Output] = GetFrame( obj )
      % Local Data
      vResult = 0;
      pResult = libpointer( 'uint32Ptr', vResult );

      % Call function
      calllib( 'ViconDataStreamSDK_MATLAB', 'GetFrame_v2', obj.InstanceID, pResult );

      % Copy out data
      cResult = Result( get( pResult, 'Value' ) );
      
      Output = struct( 'Result', cResult );
      
    end

%% GetFrameNumber
    function [Output] = GetFrameNumber( obj )
      % Local Data
      vResult = 0;
      pResult = libpointer( 'uint32Ptr', vResult );
      vFrameNumber = 0;
      pFrameNumber = libpointer( 'uint32Ptr', vFrameNumber );

      % Call function
      calllib( 'ViconDataStreamSDK_MATLAB', 'GetFrameNumber_v2', obj.InstanceID, pFrameNumber, pResult );

      % Copy out data
      cResult      = Result( get( pResult, 'Value' ) );
      cFrameNumber = get( pFrameNumber, 'Value' );
      
      Output = struct( 'Result', cResult, 'FrameNumber', cFrameNumber );
      
    end

%% GetTimecode
    function [Output] = GetTimecode( obj )
      % Local Data
      vResult = 0;
      pResult = libpointer( 'uint32Ptr', vResult );
      vHours = 0;
      pHours = libpointer( 'uint32Ptr', vHours );
      vMinutes = 0;
      pMinutes = libpointer( 'uint32Ptr', vMinutes );
      vSeconds = 0;
      pSeconds = libpointer( 'uint32Ptr', vSeconds );
      vFrames = 0;
      pFrames = libpointer( 'uint32Ptr', vFrames );
      vSubFrame = 0;
      pSubFrame = libpointer( 'uint32Ptr', vSubFrame );
      vFieldFlag = 0;
      pFieldFlag = libpointer( 'uint32Ptr', vFieldFlag );
      vStandard = 0;
      pStandard = libpointer( 'uint32Ptr', vStandard );
      vSubFramesPerFrame = 0;
      pSubFramesPerFrame = libpointer( 'uint32Ptr', vSubFramesPerFrame );
      vUserBits = 0;
      pUserBits = libpointer( 'uint32Ptr', vUserBits );

      % Call function
      calllib( 'ViconDataStreamSDK_MATLAB', 'GetTimecode_v2', obj.InstanceID,      ...
                                                              pHours,              ...
                                                              pMinutes,            ...
                                                              pSeconds,            ...
                                                              pFrames,             ...
                                                              pSubFrame,           ...
                                                              pFieldFlag,          ...
                                                              pStandard,           ...
                                                              pSubFramesPerFrame,  ...
                                                              pUserBits,           ...  
                                                              pResult );

      % Copy out data
      cHours             =                   get( pHours,             'Value' );
      cMinutes           =                   get( pMinutes,           'Value' );
      cSeconds           =                   get( pSeconds,           'Value' );
      cFrames            =                   get( pFrames,            'Value' );
      cSubFrame          =                   get( pSubFrame,          'Value' );
      cFieldFlag         =                   get( pFieldFlag,         'Value' );
      cStandard          = TimecodeStandard( get( pStandard,          'Value' ) );
      cSubFramesPerFrame =                   get( pSubFramesPerFrame, 'Value' );
      cUserBits          =                   get( pUserBits,          'Value' );
      cResult            = Result(           get( pResult,            'Value' ) );
      
      Output = struct( 'Result',            cResult,            ...
                       'Hours',             cHours,             ...
                       'Minutes',           cMinutes,           ...
                       'Seconds',           cSeconds,           ...
                       'Frames',            cFrames,            ...
                       'SubFrame',          cSubFrame,          ...
                       'FieldFlag',         cFieldFlag,         ...
                       'Standard',          cStandard,          ...
                       'SubFramesPerFrame', cSubFramesPerFrame, ...
                       'UserBits',          cUserBits );
      
    end

%% GetFrameRate
    function [Output] = GetFrameRate( obj )
      % Local Data
      vResult = 0;
      pResult = libpointer( 'uint32Ptr', vResult );
      vValue = 0.0;
      pValue = libpointer( 'doublePtr', vValue );

      % Call function
      calllib( 'ViconDataStreamSDK_MATLAB', 'GetFrameRate', obj.InstanceID, pValue, pResult );

      % Copy out data
      cResult      = Result( get( pResult, 'Value' ) );
      cFrameRate = get( pValue, 'Value' );
      
      Output = struct( 'Result', cResult, 'FrameRateHz', cFrameRate );
      
    end


%% GetLatencySampleCount
    function [Output] = GetLatencySampleCount( obj )
      % Local Data
      vResult = 0;
      pResult = libpointer( 'uint32Ptr', vResult );
      vLatencySampleCount = 0;
      pLatencySampleCount = libpointer( 'uint32Ptr', vLatencySampleCount );

      % Call function
      calllib( 'ViconDataStreamSDK_MATLAB', 'GetLatencySampleCount_v2', obj.InstanceID, pLatencySampleCount, pResult );

      % Copy out data
      cResult      = Result( get( pResult, 'Value' ) );
      cLatencySampleCount = get( pLatencySampleCount, 'Value' );
      
      Output = struct( 'Result', cResult, 'Count', cLatencySampleCount );
      
    end

%% GetLatencySampleName
    function [Output] = GetLatencySampleName( obj, LatencySampleIndex )
      % Local Data
      vResult = 0;
      pResult = libpointer( 'uint32Ptr', vResult );

      % Call function
      cLatencySampleName = calllib( 'ViconDataStreamSDK_MATLAB', 'GetLatencySampleName_v2', obj.InstanceID, LatencySampleIndex, pResult );

      % Copy out data
      cResult = Result( get( pResult, 'Value' ) );
      
      Output = struct( 'Result', cResult, 'Name', cLatencySampleName );
      
    end

%% GetLatencySampleValue
    function [Output] = GetLatencySampleValue( obj, LatencySampleName )
      % Local Data
      vResult = 0;
      pResult = libpointer( 'uint32Ptr', vResult );
      vValue = 0.0;
      pValue = libpointer( 'doublePtr', vValue );

      % Call function
      calllib( 'ViconDataStreamSDK_MATLAB', 'GetLatencySampleValue_v2', obj.InstanceID, LatencySampleName, pValue, pResult );

      % Copy out data
      cResult = Result( get( pResult, 'Value' ) );
      cValue  =         get( pValue,  'Value' );
      
      Output = struct( 'Result', cResult, 'Value', cValue );
      
    end

%% GetLatencyTotal
    function [Output] = GetLatencyTotal( obj )
      % Local Data
      vResult = 0;
      pResult = libpointer( 'uint32Ptr', vResult );
      vTotal = 0.0;
      pTotal = libpointer( 'doublePtr', vTotal );

      % Call function
      calllib( 'ViconDataStreamSDK_MATLAB', 'GetLatencyTotal_v2', obj.InstanceID, pTotal, pResult );

      % Copy out data
      cResult = Result( get( pResult, 'Value' ) );
      cTotal  =         get( pTotal,  'Value' );
      
      Output = struct( 'Result', cResult, 'Total', cTotal );
      
    end

%% GetSubjectCount
    function [Output] = GetSubjectCount( obj )
      % Local Data
      vResult = 0;
      pResult = libpointer( 'uint32Ptr', vResult );
      vSubjectCount = 0;
      pSubjectCount = libpointer( 'uint32Ptr', vSubjectCount );

      % Call function
      calllib( 'ViconDataStreamSDK_MATLAB', 'GetSubjectCount_v2', obj.InstanceID, pSubjectCount, pResult );

      % Copy out data
      cResult       = Result( get( pResult, 'Value' ) );
      cSubjectCount = get( pSubjectCount, 'Value' );
      
      Output = struct( 'Result', cResult, 'SubjectCount', cSubjectCount );
      
    end


%% GetSubjectName
    function [Output] = GetSubjectName( obj, SubjectIndex )
      % Local Data
      vResult = 0;
      pResult = libpointer( 'uint32Ptr', vResult );

      % Call function
      cSubjectName = calllib( 'ViconDataStreamSDK_MATLAB', 'GetSubjectName_v2', obj.InstanceID, SubjectIndex, pResult );

      % Copy out data
      cResult = Result( get( pResult, 'Value' ) );
      
      Output = struct( 'Result', cResult, 'SubjectName', cSubjectName );
      
    end

%% GetSubjectRootSegmentName
    function [Output] = GetSubjectRootSegmentName( obj, SubjectName )
      % Local Data
      vResult = 0;
      pResult = libpointer( 'uint32Ptr', vResult );

      % Call function
      cSegmentName = calllib( 'ViconDataStreamSDK_MATLAB', 'GetSubjectRootSegmentName_v2', obj.InstanceID, SubjectName, pResult );

      % Copy out data
      cResult = Result( get( pResult, 'Value' ) );
      
      Output = struct( 'Result', cResult, 'SegmentName', cSegmentName );
      
    end

%% GetSegmentCount
    function [Output] = GetSegmentCount( obj, SubjectName )
      % Local Data
      vResult = 0;
      pResult = libpointer( 'uint32Ptr', vResult );
      vSegmentCount = 0;
      pSegmentCount = libpointer( 'uint32Ptr', vSegmentCount );

      % Call function
      calllib( 'ViconDataStreamSDK_MATLAB', 'GetSegmentCount_v2', obj.InstanceID, SubjectName, pSegmentCount, pResult );

      % Copy out data
      cResult       = Result( get( pResult, 'Value' ) );
      cSegmentCount = get( pSegmentCount, 'Value' );
      
      Output = struct( 'Result', cResult, 'SegmentCount', cSegmentCount );
      
    end

%% GetSegmentName
    function [Output] = GetSegmentName( obj, SubjectName, SegmentIndex )
      % Local Data
      vResult = 0;
      pResult = libpointer( 'uint32Ptr', vResult );

      % Call function
      cSegmentName = calllib( 'ViconDataStreamSDK_MATLAB', 'GetSegmentName_v2', obj.InstanceID, SubjectName, SegmentIndex, pResult );

      % Copy out data
      cResult = Result( get( pResult, 'Value' ) );
      
      Output = struct( 'Result', cResult, 'SegmentName', cSegmentName );
      
    end

%% GetSegmentParentName
    function [Output] = GetSegmentParentName( obj, SubjectName, SegmentName )
      % Local Data
      vResult = 0;
      pResult = libpointer( 'uint32Ptr', vResult );

      % Call function
      cSegmentName = calllib( 'ViconDataStreamSDK_MATLAB', 'GetSegmentParentName_v2', obj.InstanceID, SubjectName, SegmentName, pResult );

      % Copy out data
      cResult = Result( get( pResult, 'Value' ) );
      
      Output = struct( 'Result', cResult, 'SegmentName', cSegmentName );
      
    end

%% GetSegmentChildCount
    function [Output] = GetSegmentChildCount( obj, SubjectName, SegmentName )
      % Local Data
      vResult = 0;
      pResult = libpointer( 'uint32Ptr', vResult );
      vSegmentCount = 0;
      pSegmentCount = libpointer( 'uint32Ptr', vSegmentCount );

      % Call function
      calllib( 'ViconDataStreamSDK_MATLAB', 'GetSegmentChildCount_v2', obj.InstanceID, SubjectName, SegmentName, pSegmentCount, pResult );

      % Copy out data
      cResult       = Result( get( pResult, 'Value' ) );
      cSegmentCount = get( pSegmentCount, 'Value' );
      
      Output = struct( 'Result', cResult, 'SegmentCount', cSegmentCount );
      
    end

%% GetSegmentChildName
    function [Output] = GetSegmentChildName( obj, SubjectName, SegmentName, SegmentIndex )
      % Local Data
      vResult = 0;
      pResult = libpointer( 'uint32Ptr', vResult );

      % Call function
      cSegmentName = calllib( 'ViconDataStreamSDK_MATLAB', 'GetSegmentChildName_v2', obj.InstanceID, SubjectName, SegmentName, SegmentIndex, pResult );

      % Copy out data
      cResult = Result( get( pResult, 'Value' ) );
      
      Output = struct( 'Result', cResult, 'SegmentName', cSegmentName );
      
    end

%% GetSegmentStaticTranslation
    function [Output] = GetSegmentStaticTranslation( obj, SubjectName, SegmentName )
      % Local Data
      vResult = 0;
      pResult = libpointer( 'uint32Ptr', vResult );
      vTranslation = zeros( 1, 3 );
      pTranslation = libpointer( 'doublePtrPtr', vTranslation );

      % Call function
      calllib( 'ViconDataStreamSDK_MATLAB', 'GetSegmentStaticTranslation_v2', obj.InstanceID, SubjectName, SegmentName, pTranslation, pResult );

      % Copy out data
      cResult      = Result( get( pResult, 'Value' ) );
      cTranslation = get( pTranslation, 'Value' );
      cTranslation = cTranslation';
            
      Output = struct( 'Result', cResult, 'Translation', cTranslation );
      
    end

%% GetSegmentStaticRotationHelical
    function [Output] = GetSegmentStaticRotationHelical( obj, SubjectName, SegmentName )
      % Local Data
      vResult = 0;
      pResult = libpointer( 'uint32Ptr', vResult );
      vRotation = zeros( 1, 3 );
      pRotation = libpointer( 'doublePtrPtr', vRotation );

      % Call function
      calllib( 'ViconDataStreamSDK_MATLAB', 'GetSegmentStaticRotationHelical_v2', obj.InstanceID, SubjectName, SegmentName, pRotation, pResult );

      % Copy out data
      cResult   = Result( get( pResult, 'Value' ) );
      cRotation = get( pRotation, 'Value' );
      cRotation = cRotation';
            
      Output = struct( 'Result', cResult, 'Rotation', cRotation );
      
    end

%% GetSegmentStaticRotationMatrix
    function [Output] = GetSegmentStaticRotationMatrix( obj, SubjectName, SegmentName )
      % Local Data
      vResult = 0;
      pResult = libpointer( 'uint32Ptr', vResult );
      vRotation = zeros( 3, 3 );
      pRotation = libpointer( 'doublePtrPtr', vRotation );

      % Call function
      calllib( 'ViconDataStreamSDK_MATLAB', 'GetSegmentStaticRotationMatrix_v2', obj.InstanceID, SubjectName, SegmentName, pRotation, pResult );

      % Copy out data
      cResult   = Result( get( pResult, 'Value' ) );
      cRotation = get( pRotation, 'Value' );
            
      Output = struct( 'Result', cResult, 'Rotation', cRotation );
      
    end

%% GetSegmentStaticRotationQuaternion
    function [Output] = GetSegmentStaticRotationQuaternion( obj, SubjectName, SegmentName )
      % Local Data
      vResult = 0;
      pResult = libpointer( 'uint32Ptr', vResult );
      vRotation = zeros( 1, 4 );
      pRotation = libpointer( 'doublePtrPtr', vRotation );

      % Call function
      calllib( 'ViconDataStreamSDK_MATLAB', 'GetSegmentStaticRotationQuaternion_v2', obj.InstanceID, SubjectName, SegmentName, pRotation, pResult );

      % Copy out data
      cResult   = Result( get( pResult, 'Value' ) );
      cRotation = get( pRotation, 'Value' );
      cRotation = cRotation';
            
      Output = struct( 'Result', cResult, 'Rotation', cRotation );
      
    end

%% GetSegmentStaticRotationEulerXYZ
    function [Output] = GetSegmentStaticRotationEulerXYZ( obj, SubjectName, SegmentName )
      % Local Data
      vResult = 0;
      pResult = libpointer( 'uint32Ptr', vResult );
      vRotation = zeros( 1, 3 );
      pRotation = libpointer( 'doublePtrPtr', vRotation );

      % Call function
      calllib( 'ViconDataStreamSDK_MATLAB', 'GetSegmentStaticRotationEulerXYZ_v2', obj.InstanceID, SubjectName, SegmentName, pRotation, pResult );

      % Copy out data
      cResult   = Result( get( pResult, 'Value' ) );
      cRotation = get( pRotation, 'Value' );
      cRotation = cRotation';
            
      Output = struct( 'Result', cResult, 'Rotation', cRotation );
      
    end

%% GetSegmentGlobalTranslation
    function [Output] = GetSegmentGlobalTranslation( obj, SubjectName, SegmentName )
      % Local Data
      vResult = 0;
      pResult = libpointer( 'uint32Ptr', vResult );
      vTranslation = zeros( 1, 3 );
      pTranslation = libpointer( 'doublePtrPtr', vTranslation );
      vOccluded = 0;
      pOccluded = libpointer( 'uint32Ptr', vOccluded );

      % Call function
      calllib( 'ViconDataStreamSDK_MATLAB', 'GetSegmentGlobalTranslation_v2', obj.InstanceID, SubjectName, SegmentName, pTranslation, pOccluded, pResult );

      % Copy out data
      cResult      = Result( get( pResult, 'Value' ) );
      cTranslation = get( pTranslation, 'Value' );
      cTranslation = cTranslation';
      cOccluded    = get( pOccluded, 'Value' );
            
      Output = struct( 'Result', cResult, 'Translation', cTranslation, 'Occluded', cOccluded );
      
    end

%% GetSegmentGlobalRotationHelical
    function [Output] = GetSegmentGlobalRotationHelical( obj, SubjectName, SegmentName )
      % Local Data
      vResult = 0;
      pResult = libpointer( 'uint32Ptr', vResult );
      vRotation = zeros( 1, 3 );
      pRotation = libpointer( 'doublePtrPtr', vRotation );
      vOccluded = 0;
      pOccluded = libpointer( 'uint32Ptr', vOccluded );

      % Call function
      calllib( 'ViconDataStreamSDK_MATLAB', 'GetSegmentGlobalRotationHelical_v2', obj.InstanceID, SubjectName, SegmentName, pRotation, pOccluded, pResult );

      % Copy out data
      cResult   = Result( get( pResult, 'Value' ) );
      cRotation = get( pRotation, 'Value' );
      cRotation = cRotation';
      cOccluded = get( pOccluded, 'Value' );
            
      Output = struct( 'Result', cResult, 'Rotation', cRotation, 'Occluded', cOccluded );
      
    end

%% GetSegmentGlobalRotationMatrix
    function [Output] = GetSegmentGlobalRotationMatrix( obj, SubjectName, SegmentName )
      % Local Data
      vResult = 0;
      pResult = libpointer( 'uint32Ptr', vResult );
      vRotation = zeros( 3, 3 );
      pRotation = libpointer( 'doublePtrPtr', vRotation );
      vOccluded = 0;
      pOccluded = libpointer( 'uint32Ptr', vOccluded );

      % Call function
      calllib( 'ViconDataStreamSDK_MATLAB', 'GetSegmentGlobalRotationMatrix_v2', obj.InstanceID, SubjectName, SegmentName, pRotation, pOccluded, pResult );

      % Copy out data
      cResult   = Result( get( pResult, 'Value' ) );
      cRotation = get( pRotation, 'Value' );
      cOccluded = get( pOccluded, 'Value' );
            
      Output = struct( 'Result', cResult, 'Rotation', cRotation, 'Occluded', cOccluded );
      
    end

%% GetSegmentGlobalRotationQuaternion
    function [Output] = GetSegmentGlobalRotationQuaternion( obj, SubjectName, SegmentName )
      % Local Data
      vResult = 0;
      pResult = libpointer( 'uint32Ptr', vResult );
      vRotation = zeros( 1, 4 );
      pRotation = libpointer( 'doublePtrPtr', vRotation );
      vOccluded = 0;
      pOccluded = libpointer( 'uint32Ptr', vOccluded );

      % Call function
      calllib( 'ViconDataStreamSDK_MATLAB', 'GetSegmentGlobalRotationQuaternion_v2', obj.InstanceID, SubjectName, SegmentName, pRotation, pOccluded, pResult );

      % Copy out data
      cResult   = Result( get( pResult, 'Value' ) );
      cRotation = get( pRotation, 'Value' );
      cRotation = cRotation';
      cOccluded = get( pOccluded, 'Value' );
            
      Output = struct( 'Result', cResult, 'Rotation', cRotation, 'Occluded', cOccluded );
      
    end

%% GetSegmentGlobalRotationEulerXYZ
    function [Output] = GetSegmentGlobalRotationEulerXYZ( obj, SubjectName, SegmentName )
      % Local Data
      vResult = 0;
      pResult = libpointer( 'uint32Ptr', vResult );
      vRotation = zeros( 1, 3 );
      pRotation = libpointer( 'doublePtrPtr', vRotation );
      vOccluded = 0;
      pOccluded = libpointer( 'uint32Ptr', vOccluded );

      % Call function
      calllib( 'ViconDataStreamSDK_MATLAB', 'GetSegmentGlobalRotationEulerXYZ_v2', obj.InstanceID, SubjectName, SegmentName, pRotation, pOccluded, pResult );

      % Copy out data
      cResult   = Result( get( pResult, 'Value' ) );
      cRotation = get( pRotation, 'Value' );
      cRotation = cRotation';
      cOccluded = get( pOccluded, 'Value' );
            
      Output = struct( 'Result', cResult, 'Rotation', cRotation, 'Occluded', cOccluded );
      
    end


%% GetSegmentLocalTranslation
    function [Output] = GetSegmentLocalTranslation( obj, SubjectName, SegmentName )
      % Local Data
      vResult = 0;
      pResult = libpointer( 'uint32Ptr', vResult );
      vTranslation = zeros( 1, 3 );
      pTranslation = libpointer( 'doublePtrPtr', vTranslation );
      vOccluded = 0;
      pOccluded = libpointer( 'uint32Ptr', vOccluded );

      % Call function
      calllib( 'ViconDataStreamSDK_MATLAB', 'GetSegmentLocalTranslation_v2', obj.InstanceID, SubjectName, SegmentName, pTranslation, pOccluded, pResult );

      % Copy out data
      cResult      = Result( get( pResult, 'Value' ) );
      cTranslation = get( pTranslation, 'Value' );
      cTranslation = cTranslation';
      cOccluded    = get( pOccluded, 'Value' );
            
      Output = struct( 'Result', cResult, 'Translation', cTranslation, 'Occluded', cOccluded );
      
    end

%% GetSegmentLocalRotationHelical
    function [Output] = GetSegmentLocalRotationHelical( obj, SubjectName, SegmentName )
      % Local Data
      vResult = 0;
      pResult = libpointer( 'uint32Ptr', vResult );
      vRotation = zeros( 1, 3 );
      pRotation = libpointer( 'doublePtrPtr', vRotation );
      vOccluded = 0;
      pOccluded = libpointer( 'uint32Ptr', vOccluded );

      % Call function
      calllib( 'ViconDataStreamSDK_MATLAB', 'GetSegmentLocalRotationHelical_v2', obj.InstanceID, SubjectName, SegmentName, pRotation, pOccluded, pResult );

      % Copy out data
      cResult   = Result( get( pResult, 'Value' ) );
      cRotation = get( pRotation, 'Value' );
      cRotation = cRotation';
      cOccluded = get( pOccluded, 'Value' );
            
      Output = struct( 'Result', cResult, 'Rotation', cRotation, 'Occluded', cOccluded );
      
    end

%% GetSegmentLocalRotationMatrix
    function [Output] = GetSegmentLocalRotationMatrix( obj, SubjectName, SegmentName )
      % Local Data
      vResult = 0;
      pResult = libpointer( 'uint32Ptr', vResult );
      vRotation = zeros( 3, 3 );
      pRotation = libpointer( 'doublePtrPtr', vRotation );
      vOccluded = 0;
      pOccluded = libpointer( 'uint32Ptr', vOccluded );

      % Call function
      calllib( 'ViconDataStreamSDK_MATLAB', 'GetSegmentLocalRotationMatrix_v2', obj.InstanceID, SubjectName, SegmentName, pRotation, pOccluded, pResult );

      % Copy out data
      cResult   = Result( get( pResult, 'Value' ) );
      cRotation = get( pRotation, 'Value' );
      cOccluded = get( pOccluded, 'Value' );
            
      Output = struct( 'Result', cResult, 'Rotation', cRotation, 'Occluded', cOccluded );
      
    end

%% GetSegmentLocalRotationQuaternion
    function [Output] = GetSegmentLocalRotationQuaternion( obj, SubjectName, SegmentName )
      % Local Data
      vResult = 0;
      pResult = libpointer( 'uint32Ptr', vResult );
      vRotation = zeros( 1, 4 );
      pRotation = libpointer( 'doublePtrPtr', vRotation );
      vOccluded = 0;
      pOccluded = libpointer( 'uint32Ptr', vOccluded );

      % Call function
      calllib( 'ViconDataStreamSDK_MATLAB', 'GetSegmentLocalRotationQuaternion_v2', obj.InstanceID, SubjectName, SegmentName, pRotation, pOccluded, pResult );

      % Copy out data
      cResult   = Result( get( pResult, 'Value' ) );
      cRotation = get( pRotation, 'Value' );
      cRotation = cRotation';
      cOccluded = get( pOccluded, 'Value' );
            
      Output = struct( 'Result', cResult, 'Rotation', cRotation, 'Occluded', cOccluded );
      
    end

%% GetSegmentLocalRotationEulerXYZ
    function [Output] = GetSegmentLocalRotationEulerXYZ( obj, SubjectName, SegmentName )
      % Local Data
      vResult = 0;
      pResult = libpointer( 'uint32Ptr', vResult );
      vRotation = zeros( 1, 3 );
      pRotation = libpointer( 'doublePtrPtr', vRotation );
      vOccluded = 0;
      pOccluded = libpointer( 'uint32Ptr', vOccluded );

      % Call function
      calllib( 'ViconDataStreamSDK_MATLAB', 'GetSegmentLocalRotationEulerXYZ_v2', obj.InstanceID, SubjectName, SegmentName, pRotation, pOccluded, pResult );

      % Copy out data
      cResult   = Result( get( pResult, 'Value' ) );
      cRotation = get( pRotation, 'Value' );
      cRotation = cRotation';
      cOccluded = get( pOccluded, 'Value' );
            
      Output = struct( 'Result', cResult, 'Rotation', cRotation, 'Occluded', cOccluded );
      
    end

%% GetMarkerCount
    function [Output] = GetMarkerCount( obj, SubjectName )
      % Local Data
      vResult = 0;
      pResult = libpointer( 'uint32Ptr', vResult );
      vMarkerCount = 0;
      pMarkerCount = libpointer( 'uint32Ptr', vMarkerCount );

      % Call function
      calllib( 'ViconDataStreamSDK_MATLAB', 'GetMarkerCount_v2', obj.InstanceID, SubjectName, pMarkerCount, pResult );

      % Copy out data
      cResult      = Result( get( pResult, 'Value' ) );
      cMarkerCount = get( pMarkerCount, 'Value' );
      
      Output = struct( 'Result', cResult, 'MarkerCount', cMarkerCount );
      
    end

%% GetMarkerName
    function [Output] = GetMarkerName( obj, SubjectName, MarkerIndex )
      % Local Data
      vResult = 0;
      pResult = libpointer( 'uint32Ptr', vResult );

      % Call function
      cMarkerName = calllib( 'ViconDataStreamSDK_MATLAB', 'GetMarkerName_v2', obj.InstanceID, SubjectName, MarkerIndex, pResult );

      % Copy out data
      cResult = Result( get( pResult, 'Value' ) );
      
      Output = struct( 'Result', cResult, 'MarkerName', cMarkerName );
      
    end

%% GetMarkerParentName
    function [Output] = GetMarkerParentName( obj, SubjectName, MarkerName )
      % Local Data
      vResult = 0;
      pResult = libpointer( 'uint32Ptr', vResult );

      % Call function
      cSegmentName = calllib( 'ViconDataStreamSDK_MATLAB', 'GetMarkerParentName_v2', obj.InstanceID, SubjectName, MarkerName, pResult );

      % Copy out data
      cResult = Result( get( pResult, 'Value' ) );
      
      Output = struct( 'Result', cResult, 'SegmentName', cSegmentName );
      
    end

%% GetMarkerGlobalTranslation
    function [Output] = GetMarkerGlobalTranslation( obj, SubjectName, MarkerName )
      % Local Data
      vResult = 0;
      pResult = libpointer( 'uint32Ptr', vResult );
      vTranslation = zeros( 1, 3 );
      pTranslation = libpointer( 'doublePtrPtr', vTranslation );
      vOccluded = 0;
      pOccluded = libpointer( 'uint32Ptr', vOccluded );

      % Call function
      calllib( 'ViconDataStreamSDK_MATLAB', 'GetMarkerGlobalTranslation_v2', obj.InstanceID, SubjectName, MarkerName, pTranslation, pOccluded, pResult );

      % Copy out data
      cResult      = Result( get( pResult, 'Value' ) );
      cTranslation = get( pTranslation, 'Value' );
      cTranslation = cTranslation';
      cOccluded    = get( pOccluded, 'Value' );
            
      Output = struct( 'Result', cResult, 'Translation', cTranslation, 'Occluded', cOccluded );
      
    end

%% GetUnlabeledMarkerCount
    function [Output] = GetUnlabeledMarkerCount( obj )
      % Local Data
      vResult = 0;
      pResult = libpointer( 'uint32Ptr', vResult );
      vMarkerCount = 0;
      pMarkerCount = libpointer( 'uint32Ptr', vMarkerCount );

      % Call function
      calllib( 'ViconDataStreamSDK_MATLAB', 'GetUnlabeledMarkerCount_v2', obj.InstanceID, pMarkerCount, pResult );

      % Copy out data
      cResult      = Result( get( pResult, 'Value' ) );
      cMarkerCount = get( pMarkerCount, 'Value' );
      
      Output = struct( 'Result', cResult, 'MarkerCount', cMarkerCount );
      
    end

%% GetUnlabeledMarkerGlobalTranslation
    function [Output] = GetUnlabeledMarkerGlobalTranslation( obj, MarkerIndex )
      % Local Data
      vResult = 0;
      pResult = libpointer( 'uint32Ptr', vResult );
      vTranslation = zeros( 1, 3 );
      pTranslation = libpointer( 'doublePtrPtr', vTranslation );

      % Call function
      calllib( 'ViconDataStreamSDK_MATLAB', 'GetUnlabeledMarkerGlobalTranslation_v2', obj.InstanceID, MarkerIndex, pTranslation, pResult );

      % Copy out data
      cResult      = Result( get( pResult, 'Value' ) );
      cTranslation = get( pTranslation, 'Value' );
      cTranslation = cTranslation';
            
      Output = struct( 'Result', cResult, 'Translation', cTranslation );
      
    end

%% GetDeviceCount
    function [Output] = GetDeviceCount( obj )
      % Local Data
      vResult = 0;
      pResult = libpointer( 'uint32Ptr', vResult );
      vDeviceCount = 0;
      pDeviceCount = libpointer( 'uint32Ptr', vDeviceCount );

      % Call function
      calllib( 'ViconDataStreamSDK_MATLAB', 'GetDeviceCount_v2', obj.InstanceID, pDeviceCount, pResult );

      % Copy out data
      cResult      = Result( get( pResult, 'Value' ) );
      cDeviceCount = get( pDeviceCount, 'Value' );
      
      Output = struct( 'Result', cResult, 'DeviceCount', cDeviceCount );
      
    end

%% GetDeviceName
    function [Output] = GetDeviceName( obj, DeviceIndex )
      % Local Data
      vResult = 0;
      pResult = libpointer( 'uint32Ptr', vResult );
      vDeviceType = 0;
      pDeviceType = libpointer( 'uint32Ptr', vDeviceType );

      % Call function
      cDeviceName = calllib( 'ViconDataStreamSDK_MATLAB', 'GetDeviceName_v2', obj.InstanceID, DeviceIndex, pDeviceType, pResult );

      % Copy out data
      cResult     = Result(     get( pResult,     'Value' ) );
      cDeviceType = DeviceType( get( pDeviceType, 'Value' ) );
      
      Output = struct( 'Result', cResult, 'DeviceName', cDeviceName, 'DeviceType', cDeviceType );
      
    end

%% GetDeviceOutputCount
    function [Output] = GetDeviceOutputCount( obj, DeviceName )
      % Local Data
      vResult = 0;
      pResult = libpointer( 'uint32Ptr', vResult );
      vDeviceOutputCount = 0;
      pDeviceOutputCount = libpointer( 'uint32Ptr', vDeviceOutputCount );

      % Call function
      calllib( 'ViconDataStreamSDK_MATLAB', 'GetDeviceOutputCount_v2', obj.InstanceID, DeviceName, pDeviceOutputCount, pResult );

      % Copy out data
      cResult            = Result( get( pResult, 'Value' ) );
      cDeviceOutputCount = get( pDeviceOutputCount, 'Value' );
      
      Output = struct( 'Result', cResult, 'DeviceOutputCount', cDeviceOutputCount );
      
    end

%% GetDeviceOutputName
    function [Output] = GetDeviceOutputName( obj, DeviceName, DeviceOutputIndex )
      % Local Data
      vResult = 0;
      pResult = libpointer( 'uint32Ptr', vResult );
      vUnit = 0;
      pUnit = libpointer( 'uint32Ptr', vUnit );

      % Call function
      cDeviceOutputName = calllib( 'ViconDataStreamSDK_MATLAB', 'GetDeviceOutputName_v2', obj.InstanceID, DeviceName, DeviceOutputIndex, pUnit, pResult );

      % Copy out data
      cResult = Result( get( pResult, 'Value' ) );
      cUnit   = Unit(   get( pUnit,   'Value' ) );
     
      Output = struct( 'Result', cResult, 'DeviceOutputName', cDeviceOutputName, 'DeviceOutputUnit', cUnit );
     
    end

%% GetDeviceOutputSubsamples
    function [Output] = GetDeviceOutputSubsamples( obj, DeviceName, DeviceOutputName )
      % Local Data
      vResult = 0;
      pResult = libpointer( 'uint32Ptr', vResult );
      vDeviceOutputSubsamples = 0;
      pDeviceOutputSubsamples = libpointer( 'uint32Ptr', vDeviceOutputSubsamples );
      vOccluded = 0;
      pOccluded = libpointer( 'uint32Ptr', vOccluded );

      % Call function
      calllib( 'ViconDataStreamSDK_MATLAB', 'GetDeviceOutputSubsamples_v2', obj.InstanceID, DeviceName, DeviceOutputName, pDeviceOutputSubsamples, pOccluded, pResult );

      % Copy out data
      cResult     = Result( get( pResult, 'Value' ) );
      cDeviceOutputSubsamples = get( pDeviceOutputSubsamples, 'Value' );
      cOccluded   = get( pOccluded, 'Value' );
           
      Output = struct( 'Result', cResult, 'DeviceOutputSubsamples', cDeviceOutputSubsamples, 'Occluded', cOccluded );
     
    end

%% GetDeviceOutputValue
    function [Output] = GetDeviceOutputValue( obj, DeviceName, DeviceOutputName, Subsample )
      % Default subsample to 1 if not supplied.
      if ( nargin == 3 )
        Subsample = 1;
      end
      
      % Local Data
      vResult = 0;
      pResult = libpointer( 'uint32Ptr', vResult );
      vValue = 0.0;
      pValue = libpointer( 'doublePtrPtr', vValue );
      vOccluded = 0;
      pOccluded = libpointer( 'uint32Ptr', vOccluded );

      % Call function
      calllib( 'ViconDataStreamSDK_MATLAB', 'GetDeviceOutputSubsample_v2', obj.InstanceID, DeviceName, DeviceOutputName, Subsample, pValue, pOccluded, pResult );

      % Copy out data
      cResult   = Result( get( pResult, 'Value' ) );
      cValue    = get( pValue, 'Value' );
      cOccluded = get( pOccluded, 'Value' );
           
      Output = struct( 'Result', cResult, 'Value', cValue, 'Occluded', cOccluded );
     
    end

%% GetForcePlateCount
    function [Output] = GetForcePlateCount( obj )
      % Local Data
      vResult = 0;
      pResult = libpointer( 'uint32Ptr', vResult );
      vForcePlateCount = 0;
      pForcePlateCount = libpointer( 'uint32Ptr', vForcePlateCount );

      % Call function
      calllib( 'ViconDataStreamSDK_MATLAB', 'GetForcePlateCount_v2', obj.InstanceID, pForcePlateCount, pResult );

      % Copy out data
      cResult   = Result( get( pResult, 'Value' ) );      
      cForcePlateCount = get( pForcePlateCount, 'Value' );
      
      Output = struct( 'Result', cResult, 'ForcePlateCount', cForcePlateCount );
      
    end

%% GetForcePlateSubsamples
    function [Output] = GetForcePlateSubsamples( obj, ForcePlateIndex )
      % Local Data
      vResult = 0;
      pResult = libpointer( 'uint32Ptr', vResult );
      vForcePlateSubsamples = 0;
      pForcePlateSubsamples = libpointer( 'uint32Ptr', vForcePlateSubsamples );

      % Call function
      calllib( 'ViconDataStreamSDK_MATLAB', 'GetForcePlateSubsamples_v2', obj.InstanceID, ForcePlateIndex, pForcePlateSubsamples, pResult );

      % Copy out data
      cResult   = Result( get( pResult, 'Value' ) );      
      cForcePlateSubsamples = get( pForcePlateSubsamples, 'Value' );
      
      Output = struct( 'Result', cResult, 'ForcePlateSubsamples', cForcePlateSubsamples );
      
    end

%% GetGlobalForceVector
    function [Output] = GetGlobalForceVector( obj, ForcePlateIndex, Subsample )
      % Default subsample to 1 if not supplied.
      if ( nargin == 2 )
        Subsample = 1;
      end
      
      % Local Data
      vResult = 0;
      pResult = libpointer( 'uint32Ptr', vResult );
      vForceVector = zeros( 1, 3 );
      pForceVector = libpointer( 'doublePtrPtr', vForceVector );

      % Call function
      calllib( 'ViconDataStreamSDK_MATLAB', 'GetGlobalForceVectorSubsample_v2', obj.InstanceID, ForcePlateIndex, Subsample, pForceVector, pResult );

      % Copy out data
      cResult      = Result( get( pResult, 'Value' ) );
      cForceVector = get( pForceVector, 'Value' );
      cForceVector = cForceVector';
            
      Output = struct( 'Result', cResult, 'ForceVector', cForceVector );
      
    end

%% GetGlobalMomentVector
    function [Output] = GetGlobalMomentVector( obj, ForcePlateIndex, Subsample )
      % Default subsample to 1 if not supplied.
      if ( nargin == 2 )
        Subsample = 1;
      end
      
      % Local Data
      vResult = 0;
      pResult = libpointer( 'uint32Ptr', vResult );
      vMomentVector = zeros( 1, 3 );
      pMomentVector = libpointer( 'doublePtrPtr', vMomentVector );

      % Call function
      calllib( 'ViconDataStreamSDK_MATLAB', 'GetGlobalMomentVectorSubsample_v2', obj.InstanceID, ForcePlateIndex, Subsample, pMomentVector, pResult );

      % Copy out data
      cResult      = Result( get( pResult, 'Value' ) );
      cMomentVector = get( pMomentVector, 'Value' );
      cMomentVector = cMomentVector';
            
      Output = struct( 'Result', cResult, 'MomentVector', cMomentVector );
      
    end
    
%% GetGlobalCentreOfPressure
    function [Output] = GetGlobalCentreOfPressure( obj, ForcePlateIndex, Subsample )
      % Default subsample to 1 if not supplied.
      if ( nargin == 2 )
        Subsample = 1;
      end

      % Local Data
      vResult = 0;
      pResult = libpointer( 'uint32Ptr', vResult );
      vCentreOfPressure = zeros( 1, 3 );
      pCentreOfPressure = libpointer( 'doublePtrPtr', vCentreOfPressure );

      % Call function
      calllib( 'ViconDataStreamSDK_MATLAB', 'GetGlobalCentreOfPressureSubsample_v2', obj.InstanceID, ForcePlateIndex, Subsample, pCentreOfPressure, pResult );

      % Copy out data
      cResult      = Result( get( pResult, 'Value' ) );
      cCentreOfPressure = get( pCentreOfPressure, 'Value' );
      cCentreOfPressure = cCentreOfPressure';
            
      Output = struct( 'Result', cResult, 'CentreOfPressure', cCentreOfPressure );
      
    end
    

%% GetEyeTrackerCount
    function [Output] = GetEyeTrackerCount( obj )
      % Local Data
      vResult          = 0;
      pResult          = libpointer( 'uint32Ptr', vResult );
      vEyeTrackerCount = 0;
      pEyeTrackerCount = libpointer( 'uint32Ptr', vEyeTrackerCount );

      % Call function
      calllib( 'ViconDataStreamSDK_MATLAB', 'GetEyeTrackerCount_v2', obj.InstanceID, pEyeTrackerCount, pResult );

      % Copy out data
      cResult          = Result( get( pResult, 'Value' ) );      
      cEyeTrackerCount = get( pEyeTrackerCount, 'Value' );
      
      Output = struct( 'Result', cResult, 'EyeTrackerCount', cEyeTrackerCount );
      
    end

%% GetEyeTrackerGlobalPosition
    function [Output] = GetEyeTrackerGlobalPosition( obj, EyeTrackerIndex )
      % Local Data
      vResult   = 0;
      pResult   = libpointer( 'uint32Ptr', vResult );
      vPosition = zeros( 1, 3 );
      pPosition = libpointer( 'doublePtrPtr', vPosition );
      vOccluded = 0;
      pOccluded = libpointer( 'uint32Ptr', vOccluded ); 

      % Call function
      calllib( 'ViconDataStreamSDK_MATLAB', 'GetEyeTrackerGlobalPosition_v2', obj.InstanceID, EyeTrackerIndex, pPosition, pOccluded, pResult );

      % Copy out data
      cResult   = Result( get( pResult, 'Value' ) );
      cPosition = get( pPosition, 'Value' );
      cPosition = cPosition';
      cOccluded = get( pOccluded, 'Value' );
            
      Output = struct( 'Result', cResult, 'Position', cPosition, 'Occluded', cOccluded );
      
    end

%% GetEyeTrackerGlobalGazeVector
    function [Output] = GetEyeTrackerGlobalGazeVector( obj, EyeTrackerIndex )
      % Local Data
      vResult     = 0;
      pResult     = libpointer( 'uint32Ptr', vResult );
      vGazeVector = zeros( 1, 3 );
      pGazeVector = libpointer( 'doublePtrPtr', vGazeVector );
      vOccluded   = 0;
      pOccluded   = libpointer( 'uint32Ptr', vOccluded ); 

      % Call function
      calllib( 'ViconDataStreamSDK_MATLAB', 'GetEyeTrackerGlobalGazeVector_v2', obj.InstanceID, EyeTrackerIndex, pGazeVector, pOccluded, pResult );

      % Copy out data
      cResult     = Result( get( pResult, 'Value' ) );
      cGazeVector = get( pGazeVector, 'Value' );
      cGazeVector = cGazeVector';
      cOccluded   = get( pOccluded, 'Value' );
            
      Output = struct( 'Result', cResult, 'GazeVector', cGazeVector, 'Occluded', cOccluded );
      
    end


    
  end% methods
  
end% classdef
