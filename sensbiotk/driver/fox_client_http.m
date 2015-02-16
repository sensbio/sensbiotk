function [data]=fox_client_http

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%% FOX NODE HTTP CLIENT %%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Script for sending a GET request
% to the FOX PYTHON HTTP SERVER.
% The request reads real time data
% from one IMU connected to the
% FOX sink node.

% Author : Benoît SIJOBERT
% Copyright : INRIA 2015 (sensbiotk.v2)

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%% Initializes variables
global HOST_IP
HOST_IP = 'localhost' ;
global PORT
PORT = '8000' ;
global Period
Period = 0.001 ;
global data
data = [];
global time_init
global t1
global figure_handle
global plot_handle

%% Initializes initial time
time_init = clock; % the computer initial time

%% Creates a timer object and starts it
% Create a timer called every (Period+TimerFcn time), and
% associated to the read_data function.
t1 = timer('Period', Period, 'ExecutionMode', 'fixedSpacing','BusyMode','Queue', 'TimerFcn', {@read_data});
start(t1)

%% Creates and show a dialog box to stop the timer
h = msgbox('Stop datastream client');
movegui(h,'northeast'); 
set(h,'DeleteFcn',{@stop_stream})


%% Initializes and creates the figure for live plotting
% init_plot();


%% Here the script for processing the stream data
% while strcmp(get(t1,'Running'),'on')
%      update_plot
% end
end

function read_data(obj, event, string_arg)
%% Read the datastream through a HTTP server get request
global HOST_IP
global PORT
global data
global time_init
[data_url, status] = urlread(...
    ['http://' HOST_IP ':' PORT]);
if status
    time_read = clock;
    elapsed_time = etime(time_read, time_init)*1000; % elapsed time in ms
    data = [data; [elapsed_time sscanf(data_url,'%f',[1,9])]];
end
end

function stop_stream(obj, event, string_arg)
%% Stops the data stream and closes everything
global t1
global data
stop(t1);
real_fs = size(data,1)/(data(end,1)/1000)
close all
end

function init_plot
global figure_handle
global plot_handle
figure_handle = figure('NumberTitle','off',...
    'Name','IMU DATA',...
    'Color',[0 0 0],'Visible','on','DeleteFcn',{@stop_stream});
% Set axes
axes_handle = axes('Parent',figure_handle,...
    'YGrid','on',...
    'YColor',[0.9725 0.9725 0.9725],...
    'XGrid','on',...
    'XColor',[0.9725 0.9725 0.9725],...
    'Color',[0 0 0]);
hold on;
plot_handle = plot(axes_handle,0,0,'Marker','.','LineWidth',1,'Color',[0 1 0]);
% Create xlabel
xlabel('Time (ms)','FontWeight','bold','FontSize',14,'Color',[1 1 0]);
% Create ylabel
ylabel('ACC DATA','FontWeight','bold','FontSize',14,'Color',[0.5 0.5 1]);
% Create title
title('IMU DATA','FontSize',15,'Color',[0 1 1]);
end

function update_plot(obj, event, string_arg)
%% Update the plot for real time visualization
global data
global plot_handle
if size(data,1)>300
    set(gca,'xlim',[data(end-300,1) data(end,1)]);
    set(plot_handle,'YData', data(end-300:end,2),'XData',data(end-300:end,1),'Color',[1 0 0]);
    set(copyobj(plot_handle,gca) ,'YData', data(end-300:end,3),'XData',data(end-300:end,1),'Color',[0 1 0]);
    set(copyobj(plot_handle,gca) ,'YData', data(end-300:end,4),'XData',data(end-300:end,1),'Color',[0 0 1]);
else
    set(gca,'xlim',[0 data(end,1)]);
    set(plot_handle,'YData', data(:,2),'XData',data(:,1),'Color',[1 0 0]);
    set(copyobj(plot_handle,gca) ,'YData', data(:,3),'XData',data(:,1),'Color',[0 1 0]);
    set(copyobj(plot_handle,gca) ,'YData', data(:,4),'XData',data(:,1),'Color',[0 0 1]);
end
drawnow;
end

