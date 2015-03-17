function pcSetIntensity(s,stimParams,maxIntensity,minIntensity,intensityScale)

fwrite(s,128,'uchar');
fwrite(s,255-128,'uchar');

for i=1:8
    thisIntensity = pcScaleIntensity(stimParams(i),maxIntensity,minIntensity,intensityScale);
    fwrite(s,thisIntensity,'uchar');
end

end

function y = pcScaleIntensity(x,maxIntensity,minIntensity,intensityScale)
    
    if (x >= maxIntensity)
        y = (maxIntensity/intensityScale) + .5;
    elseif (x <= minIntensity)
        y = (minIntensity/intensityScale) + .5;
    else
        y = (x/intensityScale) + .5;
    end
    
end