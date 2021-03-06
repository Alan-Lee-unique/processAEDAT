function handle=plot182(a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,a13,a14,a15,a16)
% Plot182 -function to handle curve plotting nicely and allow user
% to manipulate, examine, and modify plot after plotting
% using mouse commands, new menu items, and key presses.
% Arguments are passed verbatim to the built-in plot command.
% plot182 returns the figure handle.
% plot182 run with no arguments attaches menus and object handlers
% to the current figure.
%
% report bugs/suggestions to tobi@pcmp.caltech.edu

%written 3/94 by tobi delbruck for matlab 4.1
% inspired by dave gillespie's incomparably ergnomic plotting tool in his
% "view" program
% name Plot182 comes from C.A. Mead's Analog VLSI class CNS182
% at Caltech, of which i was head TA for a year.

%todo
% add automatic labeling from UserData matrix data
% improve tweak function
% fix bugs related to zombied object handlers



if nargin~=0,
	str=[];
	for i=1:nargin,
		str=[str,'a',int2str(i),','];
	end;
	str(length(str))='';
	cmd=['tmp=plot(',str,');'];
	eval(cmd);
	if nargout==1,
		handle=tmp;
	end;
end

if length(get(gcf,'children'))==1, % if menus not created yet
	Plot182Menu;
	%set(gcf,'NextPlot','new','Color','w','Interruptible','yes','Pointer','arrow');
end;	

if isempty(get(get(gca,'YLabel'),'String')), ylabel '                        '; end;
if isempty(get(get(gca,'XLabel'),'String')), xlabel '                        '; end;
if isempty(get(get(gca,'Title'),'String')),  title  '                        '; end;

set(gca,'DrawMode','fast'); % see uiguide
%set(gcf,'BackingStore','off'); % see uiguide

%Plot182AddLabels; % do this in caller

Plot182Object(1); % set up object handlers
global Plot182Ran;
if isempty(Plot182Ran),
	disp('plot182 v1.3, Bugs/Suggestions to tobi@ini.phys.ethz.ch');
	if strcmp(computer,'MAC2'), 
		disp('May have to Move|Resize plot to make Measure and Zoom function correctly');
	end
end;
Plot182Ran=1;

Plot182Msg(.95,.96,'Plot182 v1.2','red','right',14);
figure(gcf);
           ±
( Wη @  @ φΪΟ @  @ cP +―Ξ	 @  @ ν( ΅ @  @ Ζ*  4V^ @  @ ΪP j?" @  @ U@h¬Ό:'@  @ ΄/  Τ~D@  @ «ΠXyuN  @ h_@¨ύ  @  0V ±ςκ  @  ΠΎPϋ9 @  @`¬
@cεΥ9 @  @ } φs  @  @ΐXΖΚ«s @  @@ϋ
@νη@ @  @ ±
( Wη @  @ φΪΟ @  @ cP +―Ξ	 @  @ ν( ΅ @  @ Ζ*  4V^ @  @ ΪP j?" @  @ U@h¬Ό:'@  @ ΄/  Τ~D@  @ «ΠXyuN  @ h_@¨ύ  @  0V ±ςκ  @  ΠΎPϋ9 @  @`¬
@cεΥ9 @  @ } φs  @  @ΐXΖΚ«s @  @@ϋ
@νη@ @  @ ±
( Wη @  @ φΪΟ @  @ cP +―Ξ	 @  @ ν( ΅ @  @ Ζ*  4V^ @  @ ΪP j?" @  @ U@h¬Ό:'@  @ ΄/  Τ~D@  @ «ΠXyuN  @ h_@¨ύ  @  0V ±ςκ  @  ΠΎPϋ9 @  @`¬
@cεΥ9 @ 