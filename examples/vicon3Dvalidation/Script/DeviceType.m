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
classdef DeviceType
  properties (Constant = true)
    Unknown    = 0;
    ForcePlate = 1;
    EyeTracker = 2;
  end
  
  properties
    Value
  end
  
  methods
    function obj = DeviceType( value )
      obj.Value = value;
    end% Constructor
    
    function String = ToString( obj )
      switch obj.Value 
        case DeviceType.Unknown
          String = 'Unknown';
        case DeviceType.ForcePlate
          String = 'ForcePlate';
        case DeviceType.EyeTracker
          String = 'EyeTracker';          
        otherwise
          String = 'Unknown';
      end  
    end    
    
  end% methods
  
end% classdef
