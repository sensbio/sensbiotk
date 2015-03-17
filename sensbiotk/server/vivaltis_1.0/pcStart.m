function pcStart(s)

% Send command to choose low-level control
%cmdFrameInitialize.cmdId = uint8(hex2dec('13'))
%cmdFrameInitialize.length = uint8(1)
%cmdFrameInitialize.data = uint8(0)
%cmdFrameInitialize.crc = uint16(hex2dec('CAFE'))

cmdId   = uint8( hex2dec('13') )        % Initialization command
length  = uint8(1)
data    = uint8(0)
crc     = uint16( hex2dec('CAFE') )

%['13';'01';'00';'CA';'FE']
%cmdFrameInitialize = hex2dec(CmdFrameInitialize)
cmdFrame = [cmdId length data typecast(crc, 'uint8') ]

fwrite(s,CmdFrameInitialize,'uint8');

end