function fox_node_http_client

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%% FOX NODE HTTP CLIENT %%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Script for sending a GET request
% to the FOX PYTHON HTTP SERVER.
% The request reads real time data
% from one IMU connected to the
% FOX sink node.

% Author : Benoît SIJOBERT
% Last mod : 11/02/2015 11:29
% Copyright : INRIA 2015 (sensbiotk.v2)

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%% Initializes variables
global HOST_IP
HOST_IP = '127.0.0.1' ;
global PORT
PORT = '50000' ;
global Fs
Fs = 200 ;
global data
data = [];
global time_init
global t1
global t2
global figure_handle
global plot_handle

%% Initializes initial time
time_init = clock; % the computer initial time
%% Creates a timer object and starts it
% Create two timers:
% one called every 1/Fs period, at fixed interval, and
% associating the read_data function.
% the other one is used to plot data
t1 = timer('Period', 1/Fs, 'ExecutionMode', 'fixedSpacing', 'TimerFcn', {@read_data});
start(t1)
t2 = timer('Period', 1/50, 'ExecutionMode', 'fixedRate', 'TimerFcn', {@update_plot});
start(t2)

%% Creates and show a dialog box to stop the timer
h = msgbox('Stop datastream client');
set(h,'deleteFcn',{@stop_stream})

%% Initializes and create the figure for live plotting
init_plot();

end

function read_data(obj, event, string_arg)
%% Read the datastream through a HTTP server get request

global HOST_IP
global PORT
global data
global time_init
[data_url, status] = urlread(...
    ['http://' HOST_IP ':' PORT],...
    'get', ...
    {'term','urlread'});
if status
    time_read = clock;
    elapsed_time = etime(time_read, time_init)*1000; % elapsed time in ms
    data = [data; [elapsed_time sscanf(data_url,'%f',[1,9])]];
%     sscanf(data_url,'%f',[1,9])
end
end

function stop_stream(obj, event, string_arg)
%% Stops the data stream and closes everything
global t1
stop(t1);
global t2
stop(t2);
close all
clear all
end

function init_plot
global figure_handle
global plot_handle
figure_handle = figure('NumberTitle','off',...
    'Name','IMU DATA',...
    'Color',[0 0 0],'Visible','off','DeleteFcn',{@stop_stream});

% Set axes
axes_handle = axes('Parent',figure_handle,...
    'YGrid','on',...
    'YColor',[0.9725 0.9725 0.9725],...
    'XGrid','on',...
    'XColor',[0.9725 0.9725 0.9725],...
    'Color',[0 0 0]);

hold on;
plot_handle = plot(axes_handle,0,0,'Marker','.','LineWidth',1,'Color',[0 1 0]);
xlim(axes_handle,[0 2000]);
% Create xlabel
xlabel('Time (ms)','FontWeight','bold','FontSize',14,'Color',[1 1 0]);
% Create ylabel
ylabel('ACC DATA','FontWeight','bold','FontSize',14,'Color',[1 1 0]);
% Create title
title('IMU DATA','FontSize',15,'Color',[1 1 0]);
end

function update_plot(obj, event, string_arg)
%% Update the plot for real time visualization
global data
global plot_handle
global figure_handle
if size(data,1)>300
    set(gca,'xlim',[data(end-300,1) data(end,1)]);
    set(plot_handle,'YData', data(end-300:end,2),'XData',data(end-300:end,1),'Color',[1 0 0]);
    set(copyobj(plot_handle,gca) ,'YData', data(end-300:end,3),'XData',data(end-300:end,1),'Color',[0 1 0]);
    set(copyobj(plot_handle,gca) ,'YData', data(end-300:end,4),'XData',data(end-300:end,1),'Color',[0 0 1]);
    set(figure_handle,'Visible','on');
else
    set(gca,'xlim',[0 data(end,1)]);
    set(plot_handle,'YData', data(:,2),'XData',data(:,1),'Color',[1 0 0]);
    set(copyobj(plot_handle,gca) ,'YData', data(:,3),'XData',data(:,1),'Color',[0 1 0]);
    set(copyobj(plot_handle,gca) ,'YData', data(:,4),'XData',data(:,1),'Color',[0 0 1]);
    set(figure_handle,'Visible','on');
end
end
