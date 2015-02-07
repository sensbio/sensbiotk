%% Synchro IMU , Test au PRAM le 20/09/12
% 
% La calibration des acc est inutile.
% Pas de calibration électrique de GYR : on considère que l'offset est
% négligeable sur cette version des capteurs
% ici la calib des MAG n'a pas été écrite

clear
close all


% modifier le chemin d'acces au répertoire choisi path_data
% choisir le nom du fichier .mat et modifier manip en conséquence
file_name_save = 'wlkimushankR';

%% Import data

% IMU
%IMU = importdata(['wlkimushankR.csv']);
% Modification for Octave
IMU = load(['wlkimushankR.csv']);
if isstruct(IMU); IMU = IMU.data; end
time_IMU = IMU(:,2);
ACC_IMU = IMU(:,4:6);
ACC_IMU(:,4) = sqrt(sum(ACC_IMU(:,1:3).^2,2)); % norm
GYR_IMU = IMU(:,10:12);
GYR_IMU(:,4) = sqrt(sum(GYR_IMU(:,1:3).^2,2)); % norm
MAG_IMU = IMU(:,7:9);
MAG_IMU(:,4) = sqrt(sum(MAG_IMU(:,1:3).^2,2)); % norm



figure(1)
subplot(121)
plot(time_IMU,ACC_IMU(:,1:3))
ylabel('ACC')
xlabel('time (s)')
subplot(122)
plot(time_IMU,GYR_IMU(:,1:3))
ylabel('GYR')
xlabel('time (s)')



    
% Hold and Sample
    fs = 100; % Hz
    tmin = max([time_IMU(1)]);
    if mod(tmin,1/fs)~=0, tmin = tmin-mod(tmin,1/fs)+1/fs; end
    tmax = min([time_IMU(end)]);
    time = (tmin:(1/fs):tmax)';
    [~, id] = histc(time, time_IMU);
    MAG_IMU = MAG_IMU(id,:);
    ACC_IMU = ACC_IMU(id,:);
    GYR_IMU = GYR_IMU(id,:);
  
    
    
%% Unités

% Exprimer les vitesses de rotations en degrés par seconde
GYR_IMU = GYR_IMU*180/pi;


%% Sauver le ficher global

save([file_name_save '.mat'],'time','MAG_IMU','ACC_IMU','GYR_IMU');

