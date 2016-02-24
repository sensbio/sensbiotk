clear all
close all

% files=dir('H:\bsijober\ENREGISTREMENTS\STRIDE_LENGTH_GDR_WITH_WITHOUT_STIM_23102014\Data\5\EXPORT_TRACKER\LEFT_FOOT.txt');

files=dir('C:\Users\MOCAP\Desktop\sensbiotk\examples\vicon3Dvalidation\Script\Results\*.txt');


for i=1:length(files)
    datum = importdata(['Results\' files(i).name]);
    datum = datum.data;
    time = datum(:,1);
    rotX = datum(:,9)*180/pi;
    rotY = datum(:,10)*180/pi;
    rotZ = datum(:, 11)*180/pi;
    
    set(figure,'name',files(i).name);
    h(1)=subplot(311)
    plot(time, rotX, 'r','linewidth',1.5)
    legend('x')
    xlabel('Time(s)')
    ylabel('Angle(°)');
    h(2)=subplot(312)
    plot(time,rotY, 'g','linewidth',1.5)
    legend('y');
    xlabel('Time(s)')
    ylabel('Angle(°)');
    h(3)=subplot(313)
    plot(time,(rotZ-80)*-1,'linewidth',1.5)
    xlabel('Time(s)')
    ylabel('Angle(°)');
    legend('z')
    linkaxes(h,'x');
end

% set(figure,'name','Relative shank/foot angle')
% %RF
% datumRF = importdata('Results/RIGHT_FOOT.txt');
% datumRF = datumRF.data;
% timeRF = datumRF(:,1);
% rotZRF = datumRF(:, 11)*180/pi;
% rotZRF = rotZRF - rotZRF(1);
% %RS
% datumRS = importdata('Results/RIGHT_SHANK.txt');
% datumRS = datumRS.data;
% timeRS = datumRS(:,1);
% rotZRS = datumRS(:, 11)*180/pi;
% rotZRS = rotZRS - rotZRS(1);
% [timeDIFF,IRS,IRF]=intersect(timeRS,timeRF);
% rotZRS=rotZRS(IRS); rotZRF=rotZRF(IRF);
% h(1)=subplot(211);
% plot(timeDIFF, smooth(-rotZRS-rotZRF,3), 'r','linewidth',1.5)
% legend('RIGHT relative angle')
% xlabel('Time(s)')
% ylabel('Angle(°)');
% 
% 
% %LF
% datumLF = importdata('Results/LEFT_FOOT.txt');
% datumLF = datumLF.data;
% timeLF = datumLF(:,1);
% rotZLF = datumLF(:, 11)*180/pi;
% %LS
% datumLS = importdata('Results/LEFT_SHANK.txt');
% datumLS = datumLS.data;
% timeLS = datumLS(:,1);
% rotZLS = datumLS(:, 11)*180/pi;
% [timeDIFF,ILS,ILF]=intersect(timeLS,timeLF);
% rotZLS=rotZLS(ILS); rotZLF=rotZLF(ILF);
% h(2)= subplot(212);
% plot(timeDIFF, smooth(rotZLS-rotZLF,3), 'r','linewidth',1.5)
% legend('LEFT relative angle')
% xlabel('Time(s)')
% ylabel('Angle(°)');
% linkaxes(h,'x');