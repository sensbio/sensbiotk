function intensityScale = pcConfigureProstim(s,maxIntensity)

% range configuration
% 2 first bytes define command and 3rd byte configure device

fwrite(s,218,'uchar');
fwrite(s,255-218,'uchar');

if maxIntensity < 55
    fwrite(s,193,'uchar');
    intensityScale = .25;
elseif maxIntensity < 110
    fwrite(s,194,'uchar');
    intensityScale = .5;
else
    fwrite(s,195,'uchar');
    intensityScale = 1;
end

% pulse type configuration
% 2 first bytes define command and 8 following define pulse type for each channel

fwrite(s,176,'uchar');
fwrite(s,255-176,'uchar'); 

for i=1:8
    fwrite(s,0,'uchar');
end

end