function pcSetPulseWidth(s,stimParams,maxPulseWidth,minPulseWidth,pulseWidthOffset)

fwrite(s,144,'uchar');
fwrite(s,255-144,'uchar');

for i=1:8
    thisPulseWidth = pcScalePulseWidth(stimParams(i),maxPulseWidth,minPulseWidth,pulseWidthOffset);
    fwrite(s,thisPulseWidth,'uchar');
end

end

function y = pcScalePulseWidth(x,maxPulseWidth,minPulseWidth,pulseWidthOffset)
    
    if (x >= maxPulseWidth)
        y = (maxPulseWidth - pulseWidthOffset)/1.5 + .5;
    elseif (x <= minPulseWidth)
        y = (minPulseWidth - pulseWidthOffset)/1.5 + .5;
    else
        y = (x - pulseWidthOffset)/1.5 + .5;
    end
    
end