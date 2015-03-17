function pcStop(s)

global podId 
% send command to stop device
%fwrite(s,66,'uchar');
%fwrite(s,255-66,'uchar');

%pod close command
            % Create Stop frame
            cmdId           = uint8( hex2dec('31') );        % Configuration command
            length1          = uint8(2);
            targetedAppliId = uint8(1);
            crc             = uint16( hex2dec('CAFE') );

            % Send Stop frame
            requestFrame = [cmdId length1 podId targetedAppliId typecast(crc, 'uint8') ];
            fwrite(s, requestFrame, 'uint8');



% finish connection
fclose(s);

end