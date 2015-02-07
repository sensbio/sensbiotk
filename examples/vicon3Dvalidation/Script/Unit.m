%% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%
%% Copyright (C) OMG Plc 2009.
%% All rights reserved.  This software is protected by copyright
%% law and international treaties.  No part of this software / document
%% may be reproduced or distributed in any form or by any means,
%% whether transiently or incidentally to some other use of this software,
%% without the written permission of the copyright owner.
%%
%% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% Part of the ViconDataStream SDK for MATLAB.
%% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
classdef Unit
  properties (Constant = true)
    Unknown                = 0;
    Volt                   = 1;
    Newton                 = 2;
    NewtonMeter            = 3;
    Meter                  = 4;
    Kilogram               = 5;
    Second                 = 6;
    Ampere                 = 7;
    Kelvin                 = 8;
    Mole                   = 9;
    Candela                = 10;
    Radian                 = 11;
    Steradian              = 12;
    MeterSquared           = 13;
    MeterCubed             = 14;
    MeterPerSecond         = 15;
    MeterPerSecondSquared  = 16;
    RadianPerSecond        = 17;
    RadianPerSecondSquared = 18;
    Hertz                  = 19;
    Joule                  = 20;
    Watt                   = 21;
    Pascal                 = 22;
    Lumen                  = 23;
    Lux                    = 24;
    Coulomb                = 25;
    Ohm                    = 26;
    Farad                  = 27;
    Weber                  = 28;
    Tesla                  = 29;
    Henry                  = 30;
    Siemens                = 31;
    Becquerel              = 32;
    Gray                   = 33;
    Sievert                = 34;
    Katal                  = 35;
  end
  
  properties
    Value
  end
  
  methods
    function obj = Unit( value )
      obj.Value = value;
    end% Constructor
    
    function String = ToString( obj )
      switch obj.Value 
        case Unit.Unknown
          String = 'Unknown';
        case Unit.Volt
          String = 'Volt';
        case Unit.Newton
          String = 'Newton';
        case Unit.NewtonMeter
          String = 'NewtonMeter';
        case Unit.Meter
          String = 'Meter';
        case Unit.Kilogram
          String = 'Kilogram';
        case Unit.Second
          String = 'Second';
        case Unit.Ampere
          String = 'Ampere';
        case Unit.Kelvin
          String = 'Kelvin';
        case Unit.Mole
          String = 'Mole';
        case Unit.Candela
          String = 'Candela';
        case Unit.Radian
          String = 'Radian';
        case Unit.Steradian
          String = 'Steradian';
        case Unit.MeterSquared
          String = 'MeterSquared';
        case Unit.MeterCubed
          String = 'MeterCubed';
        case Unit.MeterPerSecond
          String = 'MeterPerSecond';
        case Unit.MeterPerSecondSquared
          String = 'MeterPerSecondSquared';
        case Unit.RadianPerSecond
          String = 'RadianPerSecond';
        case Unit.RadianPerSecondSquared
          String = 'RadianPerSecondSquared';
        case Unit.Hertz
          String = 'Hertz';
        case Unit.Joule
          String = 'Joule';
        case Unit.Watt
          String = 'Watt';
        case Unit.Pascal
          String = 'Pascal';
        case Unit.Lumen
          String = 'Lumen';
        case Unit.Lux
          String = 'Lux';
        case Unit.Coulomb
          String = 'Coulomb';
        case Unit.Ohm
          String = 'Ohm';
        case Unit.Farad
          String = 'Farad';
        case Unit.Weber
          String = 'Weber';
        case Unit.Tesla
          String = 'Tesla';
        case Unit.Henry
          String = 'Henry';
        case Unit.Siemens
          String = 'Siemens';
        case Unit.Becquerel
          String = 'Becquerel';
        case Unit.Gray
          String = 'Gray';
        case Unit.Sievert
          String = 'Sievert';
        case Unit.Katal
          String = 'Katal';
        otherwise
          String = 'Unknown';
      end    
    end    
    
  end% methods
  
end% classdef
