clear all
clc
clf


run extract_csv.m
%load('manip02.mat')

slidingwindowsize=10;
% ici échantillonage=100Hz
puissance_norme_acc=zeros(length(time),1);

seekforGYRzero=0;
seekforACCtresh=0;
heelon=[];
for t=slidingwindowsize/2+1:length(time)-slidingwindowsize/2
    puissance_norme_acc(t)=var(ACC_IMU(t-slidingwindowsize/2:t+slidingwindowsize/2,4));
if seekforGYRzero==0
    if -GYR_IMU(t,3)>=50
    seekforGYRzero=1;
    end
end
if seekforGYRzero==1&&seekforACCtresh==0
    if -GYR_IMU(t,3)<=0
        seekforACCtresh=1;
    end
end
if seekforGYRzero==1&&seekforACCtresh==1
    if puissance_norme_acc(t)>=20
        heelon=[heelon;t];
        seekforGYRzero=0;seekforACCtresh=0;
    end
end
end

disp(size(heelon))

figure()
ax(1)=subplot(2,1,1);
plot(time,puissance_norme_acc)
hold on
plot(time,ACC_IMU(:,4),'r')
ax(2)=subplot(2,1,2);
plot(time,GYR_IMU)
% Octave comment
% linkaxes(ax,'x')


figure()
plot(time,puissance_norme_acc)
hold on
plot(time,-GYR_IMU(:,3),'r')
plot(time(heelon'),puissance_norme_acc(heelon'),'ko')
