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
classdef TimecodeStandard
  properties (Constant = true)
    None     = 0;
    PAL      = 1;
    NTSC     = 2;
    NTSCDrop = 3;
    Film     = 4;
  end
  
  properties
    Value
  end
  
  methods
    function obj = TimecodeStandard( value )
      obj.Value = value;
    end% Constructor
    
    function String = ToString( obj )
      switch obj.Value 
        case TimecodeStandard.None
          String = 'None';
        case TimecodeStandard.PAL
          String = 'PAL';
        case TimecodeStandard.NTSC
          String = 'NTSC';
        case TimecodeStandard.NTSCDrop
          String = 'NTSCDrop';
        case TimecodeStandard.Film
          String = 'Film';
        otherwise
          String = 'None';
      end    
    end    
    
  end% methods
  
end% classdef
