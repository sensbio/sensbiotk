function pcSetPeriod(s,stimParams,maxPeriod,minPeriod)

fwrite(s,160,'uchar');
fwrite(s,255-160,'uchar');

for i=1:8
    thisPeriod = pcScalePeriod(stimParams(i),maxPeriod,minPeriod);
    fwrite(s,thisPeriod,'uchar');
end

end

function y = pcScalePeriod(x,maxPeriod,minPeriod)
    
    if (x >= maxPeriod)
        y = maxPeriod/2 + .5;
    elseif (x <= minPeriod)
        y = minPeriod/2 + .5;
    else
        y = x/2 + .5;
    end
    
end