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
classdef Direction
  properties (Constant = true)
    Up       = 0;
    Down     = 1;
    Left     = 2;
    Right    = 3;
    Forward  = 4;
    Backward = 5;
  end% properties
  
  properties
    Value
  end
  
  methods
    function obj = Direction( value )
      obj.Value = value;
    end% Constructor
    
    function String = ToString( obj )
      switch obj.Value 
        case Direction.Forward
          String = 'Forward';
        case Direction.Backward
          String = 'Backward';
        case Direction.Left
          String = 'Left';
        case Direction.Right
          String = 'Right';
        case Direction.Up
          String = 'Up';
        case Direction.Down
          String = 'Down';
        otherwise
          String = 'Unknown';
      end    
    end    
  end% methods

end% classdef
