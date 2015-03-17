function StopFcn(obj,event,s,T)

global tElapsed tStart

pcStop(s);

tElapsed = toc(tStart);
    
stop(T);
% delete(T);

% ts = timerfind;
% if length(ts) > 0
%     stop(ts);
%     delete(ts);
% end

