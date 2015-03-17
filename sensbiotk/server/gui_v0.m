function varargout = gui_v0(varargin)
gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
    'gui_Singleton',  gui_Singleton, ...
    'gui_OpeningFcn', @gui_v0_OpeningFcn, ...
    'gui_OutputFcn',  @gui_v0_OutputFcn, ...
    'gui_LayoutFcn',  [] , ...
    'gui_Callback',   []);
if nargin && ischar(varargin{1})
    gui_State.gui_Callback = str2func(varargin{1});
end

if nargout
    [varargout{1:nargout}] = gui_mainfcn(gui_State, varargin{:});
else
    gui_mainfcn(gui_State, varargin{:});
end

% --- Executes just before gui_v0 is made visible.
function gui_v0_OpeningFcn(hObject, eventdata, handles, varargin)
%% Import vivaltis comm libs
addpath(strcat(pwd,'/vivaltis_1.0/')) % loading of needed fonctions

%% Initializes variables
global HOST_IP;
HOST_IP = 'localhost';
global PORT;
PORT = '8000' ;
global Period;
Period = 0.25 ;
global handles_glob;
handles_glob = handles;

global s;
global r_set_loop;
global r_mes_loop;
global k_loop;
global intensity_loop;
global edit_intensity;
global edit_freq;
global edit_pw;
global edit_duration;


%% Timer for refreshing angle display
t1 = timer('Period', Period, 'ExecutionMode', 'fixedRate','BusyMode','queue', 'TimerFcn', @refresh_angles,'StartDelay',1);


% Choose default command line output for gui_v0
handles.output = hObject;

% Update handles structure
guidata(hObject, handles);
start(t1);

% UIWAIT makes gui_v0 wait for user response (see UIRESUME)
% uiwait(handles.figure1);


% --- Outputs from this function are returned to the command line.
function varargout = gui_v0_OutputFcn(hObject, eventdata, handles)
% varargout  cell array for returning output args (see VARARGOUT);
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Get default command line output from handles structure
varargout{1} = handles.output;


% --- Executes on button press in init_frame.
function init_frame_Callback(hObject, eventdata, handles)
global HOST_IP;
global PORT;
%% Send a http request for initializing the frame
urlread(['http://' HOST_IP ':' PORT],'Get',{'request','init'});
disp('--- FRAME INITIALIZED ---');





% --- Executes on button press in pushbutton_send_stim.
function pushbutton_send_stim_Callback(hObject, eventdata, handles)
initvivaltis();




function edit_freq_Callback(hObject, eventdata, handles)
% hObject    handle to edit_freq (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of edit_freq as text
%        str2double(get(hObject,'String')) returns contents of edit_freq as a double


% --- Executes during object creation, after setting all properties.
function edit_freq_CreateFcn(hObject, eventdata, handles)
% hObject    handle to edit_freq (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function edit_pw_Callback(hObject, eventdata, handles)


% --- Executes during object creation, after setting all properties.
function edit_pw_CreateFcn(hObject, eventdata, handles)


function edit_intensity_Callback(hObject, eventdata, handles)

% --- Executes during object creation, after setting all properties.
function edit_intensity_CreateFcn(hObject, eventdata, handles)


function pw_loop_Callback(hObject, eventdata, handles)


% --- Executes during object creation, after setting all properties.
function pw_loop_CreateFcn(hObject, eventdata, handles)


function r_mes_loop_Callback(hObject, eventdata, handles)


function r_set_loop_Callback(hObject, eventdata, handles)
global r_set_loop;
r_set_loop = st2num(get(handles.r_set_loop, 'String'));

% --- Executes during object creation, after setting all properties.
function r_set_loop_CreateFcn(hObject, eventdata, handles)



function k_loop_Callback(hObject, eventdata, handles)
global k_loop;
k_loop = str2num(get(handles.k_loop, 'String'));


% --- Executes during object creation, after setting all properties.
function k_loop_CreateFcn(hObject, eventdata, handles)
function rx_CreateFcn(hObject, eventdata, handles)
function ry_CreateFcn(hObject, eventdata, handles)
function rz_CreateFcn(hObject, eventdata, handles)
function edit_duration_CreateFcn(hObject, eventdata, handles)

% --- Executes on button press in start_command.
function start_command_Callback(hObject, eventdata, handles)
%% START LOOP




function refresh_angles(obj, event, string_arg, handles)
global handles_glob;
angles = read_angles();
set(handles_glob.rx, 'String', num2str(angles(1),'%0.1f'));
set(handles_glob.ry, 'String', num2str(angles(2),'%0.1f'));
set(handles_glob.rz, 'String', num2str(angles(3),'%0.1f'));


function angles = read_angles(obj, event, string_arg)
%% Read the angles from datastream through a HTTP server get request
global HOST_IP
global PORT
[data_url, status] = urlread(...
    ['http://' HOST_IP ':' PORT]);
if status
    data = sscanf(data_url,'%f',[1,7]);
    angles = data(1:3);
end


% --- Executes during object creation, after setting all properties.
function start_command_CreateFcn(hObject, eventdata, handles)

function init_vivaltis
%% basic POD configuration
global s;
global handles_glob;
s = pcConfigureSerial();

%% RF Controller Initialization
nPODmax = 10;
for i=1:nPODmax
    podInfo(i) = struct('type',0,'networkId',0,'state',0,'version',[0 0 0 0],'color',0);
end
pods = struct('nAvailable',0,'info',podInfo);

% Create Initialization frame and send
request.cmdId   = uint8( hex2dec('13') );        % Initialization command
request.length  = uint8(1);
request.data    = uint8(0);
request.crc     = uint16( hex2dec('CAFE') );

stimPods = struct(pods);
[strErr, pods, stimPods] = pcSendRequest_n_WaitReply(s, request, pods);

if( strcmp(strErr, 'None') )
    % Select the targeted POD
    if stimPods.nAvailable > 0
        isPodSelected = 0;
        while isPodSelected == 0
            podId = input('\n# Please Select the POD ID : ');
            podId = uint8(podId);
            i = 1;
            while (i <= stimPods.nAvailable) && ( stimPods.info(i).networkId ~= podId )
                i = i + 1;
            end
            if i <= stimPods.nAvailable
                if stimPods.info(i).networkId == podId
                    isPodSelected = 1;
                end
            end
        end
        
        fprintf('\t >> POD_%i selected \n', stimPods.info(i).networkId);
    else
        fprintf('\n # Warn : - No Available POD - \n')
        strErr = 'Exit';
    end
end

%% Targeted POD Configuration
if( strcmp(strErr, 'None') )
    % Create Configuration frame
    request.cmdId   = uint8( hex2dec('40') );        % Configuration command
    request.length  = uint8(31);
    
    outputId        = uint8(0);
    patternTypeId   = uint8( hex2dec('0B') );     % 0x0B for biphasic
    ahesionDetect   = uint8(0);
    delay           = uint8(0);
    increaseTime    = uint8(0);
    maxTime         = uint8(30);            % second
    decreaseTime    = uint8(0);
    nullTime        = uint8(0);
    set_frequency = str2num(get(handles_glob.edit_intensity, 'String'));
    frequency       = uint16(set_frequency);           % Hz
    set_frequency = str2num(get(handles_glob.edit_pw, 'String'));
    pulseWidth      = uint16(50);           % µs
    set_intensity = str2num(get(handles.edit_intensity, 'String'));
    curAmplitude    = uint16(set_intensity*10); %mA
    maxIntensity = 50;
    maxAmplitude    = uint16(maxIntensity*10);
    incrementStep   = uint8(5);             % 100 nA or 10^{-4}A
    nRepetition     = uint8(0);
    
    request.data    = [outputId podId patternTypeId ahesionDetect delay ...
        increaseTime maxTime decreaseTime nullTime ...
        typecast(frequency, 'uint8') typecast(pulseWidth, 'uint8') ...
        typecast(frequency, 'uint8') typecast(pulseWidth, 'uint8') ...
        typecast(frequency, 'uint8') typecast(pulseWidth, 'uint8') ...
        typecast(curAmplitude, 'uint8') typecast(maxAmplitude, 'uint8') ...
        incrementStep nRepetition];
    request.crc     = uint16( hex2dec('CAFE') );
    
    % Send Configuration frame
    [strErr, pods, stimPods] = pcSendRequest_n_WaitReply(s, request, pods);
    if( strcmp(strErr, 'None') )
        fprintf('\t >> POD_%i configured \n', podId)
    end
    
    if( strcmp(strErr, 'None') )
             
        %% Start POD
        % Create Start frame
        request.cmdId   = uint8( hex2dec('30') );        % Start command
        request.length  = uint8(2);      
        targetedAppliId = uint8(1);
        request.data    = [podId targetedAppliId];
        request.crc     = uint16( hex2dec('CAFE') );  
        % Send Configuration frame
        [strErr, pods, stimPods] = pcSendRequest_n_WaitReply(s, request, pods);
        if( strcmp(strErr, 'None') )
            fprintf('\t >> POD_%i started \n', podId)
        end
    end
end

% --- Executes on button press in pushbutton_stop_stim.
function pushbutton_stop_stim_Callback(hObject, eventdata, handles)
global s;
% Create Stop frame
cmdId           = uint8( hex2dec('31') );        % Configuration command
length          = uint8(2);
targetedAppliId = uint8(1);
crc             = uint16( hex2dec('CAFE') );

% Send Stop frame
requestFrame = [cmdId length podId targetedAppliId typecast(crc, 'uint8') ];
fwrite(s, requestFrame, 'uint8');

% Wait Stop reply
i = 0;
while s.BytesAvailable == 0
    i = i + 1;
end

% Get Stop reply
replyFrame = fread(s, s.BytesAvailable, 'uint8');

% Analyze the Stop reply
if( replyFrame(1) == hex2dec('55') )
    length      = replyFrame(2);
    errorType   = replyFrame(3);
    errorId     = replyFrame(4);
    podIdRe     = replyFrame(5);
    %                                 requestId   = replyFrame(6);
    
    if(errorType == 0)
        
        fprintf('\t >> POD_%i is stoped \n', podId)
    else
        'Error : Stop error !!!'
    end
else
    'Error : Invalid code id from Stop reply frame !!!'
end)
