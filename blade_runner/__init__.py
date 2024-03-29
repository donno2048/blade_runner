# Use mouse right and left click and position to play
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT']='1'
import pygame,sys,random,time,math
from copy import deepcopy
mainClock=pygame.time.Clock()
from pygame.locals import *
pygame.mixer.init()
pygame.mixer.pre_init(44100,-16,2,512)
pygame.init()
pygame.display.set_caption('blade-runner')
_m='1;1'
_l='1;0'
_k='0;1'
_j='0;0'
_i='data/font/small_font.png'
_h='.png'
_g='normal'
_f='cloud_3'
_e='cloud_2'
_d='gel'
_c='muck'
_b='down'
_a='cloud_1'
_Z='tree'
_Y=';'
_X=':'
_W='.'
_V='seeds'
_U='bush'
_T='loop'
_S='A'
_R='cloud_0'
_Q='apples'
_P='Height'
_O=' '
_N='stomper'
_M='b'
_L='blueberries'
_K='f'
_J='sword_1'
_I='sword_0'
_H='sword_3'
_G='sword_2'
_F='grass'
_E='tank'
_D='fly'
_C=True
_B=False
_A=None
WINDOWWIDTH=600
WINDOWHEIGHT=400
screen=pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT),0,32)
display=pygame.Surface((300,200))
def show_text(Text,X,Y,Spacing,WidthLimit,Font,surface,double=1,overflow=_g):
	B='\n';A='';Text+=_O;OriginalX=X;CurrentWord=A
	if overflow==_g:
		for char in Text:
			if char not in[_O,B]:
				try:CurrentWord+=str(char)
				except KeyError:pass
			else:
				WordTotal=0
				for char2 in CurrentWord:WordTotal+=Font[char2][0];WordTotal+=Spacing
				if WordTotal+X-OriginalX>WidthLimit:X=OriginalX;Y+=Font[_P]
				for char2 in CurrentWord:Image=Font[str(char2)][1];surface.blit(pygame.transform.scale(Image,(Image.get_width()*double,Image.get_height()*double)),(X*double,Y*double));X+=Font[char2][0];X+=Spacing
				if char==_O:X+=Font[_S][0];X+=Spacing
				else:X=OriginalX;Y+=Font[_P]
				CurrentWord=A
			if X-OriginalX>WidthLimit:X=OriginalX;Y+=Font[_P]
		return X,Y
	if overflow=='cut all':
		for char in Text:
			if char not in[_O,B]:
				try:Image=Font[str(char)][1];surface.blit(pygame.transform.scale(Image,(Image.get_width()*double,Image.get_height()*double)),(X*double,Y*double));X+=Font[str(char)][0];X+=Spacing
				except KeyError:pass
			else:
				if char==_O:X+=Font[_S][0];X+=Spacing
				if char==B:X=OriginalX;Y+=Font[_P]
			if X-OriginalX>WidthLimit:X=OriginalX;Y+=Font[_P]
		return X,Y
def generate_font(FontImage,FontSpacingMain,TileSize,TileSizeY,color):
	FontSpacing=deepcopy(FontSpacingMain);FontOrder=[_S,'B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','a',_M,'c','d','e',_K,'g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',_W,'-',',',_X,'+',"'",'!','?','0','1','2','3','4','5','6','7','8','9','(',')','/','_','=','\\','[',']','*','"','<','>',_Y];FontImage=pygame.image.load(FontImage).convert();NewSurf=pygame.Surface((FontImage.get_width(),FontImage.get_height())).convert();NewSurf.fill(color);FontImage.set_colorkey((0,0,0));NewSurf.blit(FontImage,(0,0));FontImage=NewSurf.copy();FontImage.set_colorkey((255,255,255));num=0
	for char in FontOrder:FontImage.set_clip(pygame.Rect((TileSize+1)*num,0,TileSize,TileSizeY));CharacterImage=FontImage.subsurface(FontImage.get_clip());FontSpacing[char].append(CharacterImage);num+=1
	FontSpacing[_P]=TileSizeY;return FontSpacing
def rot_around(surf,img,base_x,base_y,img_offset_x,img_offset_y,deg):background_img=pygame.Surface(((img.get_width()+img_offset_x)*2,(img.get_width()+img_offset_x)*2));background_img.blit(img,(img_offset_x+int(background_img.get_width()/2),int(background_img.get_width()/2)+img_offset_y));original_size=background_img.get_width(),background_img.get_height();rotated_img=pygame.transform.rotate(background_img,deg);x_inc=rotated_img.get_width()-original_size[0];y_inc=rotated_img.get_height()-original_size[1];rotated_img.set_colorkey((0,0,0));surf.blit(rotated_img,(base_x-int(original_size[0]/2)-int(x_inc/2),base_y-int(original_size[1]/2)-int(y_inc/2)))
def point_degrees(p_1,p_2):
	x=p_2[0]-p_1[0];y=p_2[1]-p_1[1];base_rotation=0
	if x<0:base_rotation=180
	if x==0:
		if y<0:return 270
		else:return 90
	else:return math.degrees(math.atan(y/x))+base_rotation
def CollisionTest(Object1,ObjectList):
	CollisionList=[]
	for Object in ObjectList:
		ObjectRect=pygame.Rect(Object[0],Object[1],Object[2],Object[3])
		if ObjectRect.colliderect(Object1):CollisionList.append(ObjectRect)
	return CollisionList
class PhysicsObject:
	def __init__(self,x,y,x_size,y_size):self.width=x_size;self.height=y_size;self.rect=pygame.Rect(x,y,self.width,self.height);self.x=x;self.y=y
	def move(self,Movement,platforms):
		D='left';C='right';B='bottom';A='top';self.x+=Movement[0];self.rect.x=int(self.x);block_hit_list=CollisionTest(self.rect,platforms);collision_types={A:_B,B:_B,C:_B,D:_B}
		for block in block_hit_list:
			if Movement[0]>0:self.rect.right=block.left;collision_types[C]=_C
			elif Movement[0]<0:self.rect.left=block.right;collision_types[D]=_C
			self.x=self.rect.x
		self.y+=Movement[1];self.rect.y=int(self.y);block_hit_list=CollisionTest(self.rect,platforms)
		for block in block_hit_list:
			if Movement[1]>0:self.rect.bottom=block.top;collision_types[B]=_C
			elif Movement[1]<0:self.rect.top=block.bottom;collision_types[A]=_C
			self.change_y=0;self.y=self.rect.y
		return collision_types
	def Draw(self):pygame.draw.rect(screen,(0,0,255),self.rect)
	def CollisionItem(self):CollisionInfo=[self.rect.x,self.rect.y,self.width,self.height];return CollisionInfo
def flip(img,boolean=_C):return pygame.transform.flip(img,boolean,_B)
class entity:
	global animation_database
	def __init__(self,x,y,size_x,size_y):self.x=x;self.y=y;self.size_x=size_x;self.size_y=size_y;self.obj=PhysicsObject(x,y,size_x,size_y);self.animation=_A;self.image=_A;self.animation_frame=0;self.animation_tags=[];self.flip=_B;self.offset=[0,0]
	def set_pos(self,x,y):self.x=x;self.y=y;self.obj.x=x;self.obj.y=y;self.obj.rect.x=x;self.obj.rect.y=y
	def move(self,momentum,platforms):collisions=self.obj.move(momentum,platforms);self.x=self.obj.x;self.y=self.obj.y;return collisions
	def rect(self):return pygame.Rect(self.x,self.y,self.size_x,self.size_y)
	def set_flip(self,boolean):self.flip=boolean
	def set_animation_tags(self,tags):self.animation_tags=tags
	def set_animation(self,sequence):self.animation=sequence;self.animation_frame=0
	def clear_animation(self):self.animation=_A
	def set_image(self,image):self.image=image
	def set_offset(self,offset):self.offset=offset
	def set_frame(self,amount):self.animation_frame=amount
	def change_frame(self,amount):
		self.animation_frame+=amount
		if self.animation!=_A:
			while self.animation_frame<0:
				if _T in self.animation_tags:self.animation_frame+=len(self.animation)
				else:self.animation=0
			while self.animation_frame>=len(self.animation):
				if _T in self.animation_tags:self.animation_frame-=len(self.animation)
				else:self.animation_frame=len(self.animation)-1
	def get_current_img(self):
		if self.animation is _A:
			if self.image is not _A:return flip(self.image,self.flip)
			else:return _A
		else:return flip(animation_database[self.animation[self.animation_frame]],self.flip)
	def display(self,surface,scroll):
		if self.animation is _A:
			if self.image is not _A:surface.blit(flip(self.image,self.flip),(int(self.x)-scroll[0]+self.offset[0],int(self.y)-scroll[1]+self.offset[1]))
		else:surface.blit(flip(animation_database[self.animation[self.animation_frame]],self.flip),(int(self.x)-scroll[0]+self.offset[0],int(self.y)-scroll[1]+self.offset[1]))
animation_database={}
def animation_sequence(sequence,base_path,colorkey=(255,255,255),transparency=255):
	global animation_database;result=[]
	for frame in sequence:
		image_id=base_path+str(frame[0]);image=pygame.image.load(image_id+_h).convert();image.set_colorkey(colorkey);image.set_alpha(transparency);animation_database[image_id]=image.copy()
		for i in range(frame[1]):result.append(image_id)
	return result
def get_frame(ID):global animation_database;return animation_database[ID]
def ms():return int(round(time.time()*1000))
def get_ms():global start_time;return int(round(time.time()*1000))-start_time
start_time=ms()
def get_text_width(text,spacing):
	global font_dat;width=0
	for char in text:
		if char in font_dat:width+=font_dat[char][0]+spacing
		elif char==_O:width+=font_dat[_S][0]+spacing
	return width
font_dat={_S:[3],'B':[3],'C':[3],'D':[3],'E':[3],'F':[3],'G':[3],'H':[3],'I':[3],'J':[3],'K':[3],'L':[3],'M':[5],'N':[3],'O':[3],'P':[3],'Q':[3],'R':[3],'S':[3],'T':[3],'U':[3],'V':[3],'W':[5],'X':[3],'Y':[3],'Z':[3],'a':[3],_M:[3],'c':[3],'d':[3],'e':[3],_K:[3],'g':[3],'h':[3],'i':[1],'j':[2],'k':[3],'l':[3],'m':[5],'n':[3],'o':[3],'p':[3],'q':[3],'r':[2],'s':[3],'t':[3],'u':[3],'v':[3],'w':[5],'x':[3],'y':[3],'z':[3],_W:[1],'-':[3],',':[2],_X:[1],'+':[3],"'":[1],'!':[1],'?':[3],'0':[3],'1':[3],'2':[3],'3':[3],'4':[3],'5':[3],'6':[3],'7':[3],'8':[3],'9':[3],'(':[2],')':[2],'/':[3],'_':[5],'=':[3],'\\':[3],'[':[2],']':[2],'*':[3],'"':[3],'<':[3],'>':[3],_Y:[1]}
font_0=generate_font(os.path.join(os.path.abspath(os.path.dirname(__file__)),_i),font_dat,5,8,(16,30,41))
font_1=generate_font(os.path.join(os.path.abspath(os.path.dirname(__file__)),_i),font_dat,5,8,(248,248,248))
def reduce(num,amount):
	if num>=amount:num-=amount
	elif num<=-amount:num+=amount
	else:num=0
	return num
def loc(x,y):return str(x)+_Y+str(y)
def ordered_render(img,pos,z=_A,secondary_sort=0):
	x=pos[0];y=pos[1];global for_render,image_cache
	if z is _A:z=y+img.get_height()
	image_cache.append(img);for_render.append([z,secondary_sort,x,y,len(image_cache)-1])
def get_nearby_tiles(pos,tiles):
	global decor;nearby_tiles=[];pos=[int(pos[0]/32),int(pos[1]/32)]
	for y in range(5):
		for x in range(5):
			pos_str=loc(pos[0]+x-2,pos[1]+y-2)
			if pos_str not in tiles:nearby_tiles.append([(pos[0]+x-2)*32,(pos[1]+y-2)*32,32,32])
			elif tiles[pos_str][3]!=0:nearby_tiles.append([(pos[0]+x-2)*32,(pos[1]+y-2)*32,32,32])
			elif pos_str in decor:nearby_tiles.append([(pos[0]+x-2)*32,(pos[1]+y-2)*32,32,32])
	return nearby_tiles
def cap(num,amount):
	if num>amount:num=amount
	if num<-amount:num=-amount
	return num
def add_img_particles(img,base_pos,blood=_C,duration=40):
	global particles;width=img.get_width();height=img.get_height()
	for y in range(height):
		for x in range(width):
			color=img.get_at((x,y))
			if color!=(255,255,255,255):
				if blood==_C:particles.append([(169,59,59),x+base_pos[0],y+base_pos[1],random.randint(0,20)/10-1,random.randint(0,20)/10-1,random.randint(10,30)])
				particles.append([color,x+base_pos[0],y+base_pos[1],0,0,random.randint(duration,int(duration*1.5))])
def flip(img,boolean):return pygame.transform.flip(img,boolean,_B).copy()
def add_item(item):
	global inventory
	for slot in inventory:
		if slot[0]==item:slot[1]+=1;return _A
	for slot in inventory:
		if slot[0]is _A:slot[0]=item;slot[1]=1;return _A
def load_snd(name):return pygame.mixer.Sound(os.path.join(os.path.abspath(os.path.dirname(__file__)),'data/sfx/')+name+'.wav')
hurt_s=load_snd('hurt')
attack_s=load_snd('attack')
dash_s=load_snd('dash')
explosion_s=load_snd('explosion')
hit_s=load_snd('hit')
hit_decor_s=load_snd('hit_decor')
attack_s.set_volume(0.5)
dash_s.set_volume(0.3)
pygame.mixer.music.load(os.path.join(os.path.abspath(os.path.dirname(__file__)),'data/music/main.wav'))
def load_img(path):img=pygame.image.load(os.path.join(os.path.abspath(os.path.dirname(__file__)),'data/images/')+path+_h).convert();img.set_colorkey((255,255,255));return img
bars_img=load_img('bars')
tile_images={_F:load_img('tiles/grass'),_c:load_img('tiles/muck')}
weapons={_I:load_img('weapons/sword_0'),_J:load_img('weapons/sword_1'),_G:load_img('weapons/sword_2'),_H:load_img('weapons/sword_3')}
decor_images={_U:[load_img('decor/bush'),-2],_L:[load_img('decor/blueberries'),-2],_Z:[load_img('decor/tree'),-18],_Q:[load_img('decor/apples'),-18]}
item_images={_L:load_img('items/blueberries'),_Q:load_img('items/apples'),_V:load_img('items/seeds'),_d:load_img('items/gel')}
slot_img=load_img('slot')
shot_img=load_img('shot')
weapon_slot=load_img('weapon_slot')
weapon_items={_I:load_img('weapon_items/sword_0'),_J:load_img('weapon_items/sword_1'),_G:load_img('weapon_items/sword_2'),_H:load_img('weapon_items/sword_3')}
controls_img=load_img('controls')
cloud_images={_R:load_img(_R),_a:load_img(_a),_e:load_img(_e),_f:load_img(_f)}
fly_stand_f=load_img('entities/fly/stand_f')
fly_stand_b=load_img('entities/fly/stand_b')
fly_fly_f=load_img('entities/fly/fly_f')
fly_fly_b=load_img('entities/fly/fly_b')
player_walk_f=animation_sequence([[0,3],[1,2],[2,3],[1,2]],os.path.join(os.path.abspath(os.path.dirname(__file__)),'data/images/entities/player/walk_f_'))
player_walk_b=animation_sequence([[0,3],[1,2],[2,3],[1,2]],os.path.join(os.path.abspath(os.path.dirname(__file__)),'data/images/entities/player/walk_b_'))
player_stand_f=load_img('entities/player/stand_f')
player_stand_b=load_img('entities/player/stand_b')
dust_anim=animation_sequence([[0,4],[1,3],[2,3],[3,4],[4,3],[5,3],[6,3],[7,3],[8,5]],os.path.join(os.path.abspath(os.path.dirname(__file__)),'data/images/misc_animations/dust_'))
tank_main_f=animation_sequence([[0,120],[1,5],[2,7],[1,5]],os.path.join(os.path.abspath(os.path.dirname(__file__)),'data/images/entities/tank/main_f_'))
tank_main_b=animation_sequence([[0,120],[1,5],[2,7],[1,5]],os.path.join(os.path.abspath(os.path.dirname(__file__)),'data/images/entities/tank/main_b_'))
stomper_stomp=animation_sequence([[0,80],[1,4],[2,4],[3,2],[4,2],[5,2],[6,2]],os.path.join(os.path.abspath(os.path.dirname(__file__)),'data/images/entities/stomper/stomp_'))
sword_0_gfx=animation_sequence([[0,1],[1,1],[2,1],[3,1],[4,1],[5,1],[6,1],[7,1],[8,1],[9,1],[10,1],[11,1],[12,1],[13,1],[14,1],[15,1],[16,1],[17,1],[18,1],[19,1],[20,1]],os.path.join(os.path.abspath(os.path.dirname(__file__)),'data/images/weapon_effects/sword_0_'))
sword_1_gfx=animation_sequence([[0,1],[1,1],[2,1],[3,1],[4,1],[5,1],[6,1],[7,1],[8,1],[9,1],[10,1],[11,1],[12,1],[13,1],[14,1],[15,1],[16,1],[17,1],[18,1],[19,1],[20,1]],os.path.join(os.path.abspath(os.path.dirname(__file__)),'data/images/weapon_effects/sword_1_'))
sword_2_gfx=animation_sequence([[0,1],[1,1],[2,1],[3,1],[4,1],[5,1],[6,1],[7,1],[8,1],[9,1],[10,1],[11,1],[12,1],[13,1],[14,1],[15,1],[16,1],[17,1],[18,1],[19,1],[20,1]],os.path.join(os.path.abspath(os.path.dirname(__file__)),'data/images/weapon_effects/sword_2_'))
sword_3_gfx=animation_sequence([[0,1],[1,1],[2,1],[3,1],[4,1],[5,1],[6,1],[7,1],[8,1],[9,1],[10,1],[11,1],[12,1],[13,1],[14,1],[15,1],[16,1],[17,1],[18,1],[19,1],[20,1]],os.path.join(os.path.abspath(os.path.dirname(__file__)),'data/images/weapon_effects/sword_3_'))
explosion_anim=animation_sequence([[0,4],[1,4],[2,4],[3,4],[4,6],[5,6],[6,6],[7,4],[8,4],[9,4],[10,4],[11,4],[12,4],[13,4],[14,4]],os.path.join(os.path.abspath(os.path.dirname(__file__)),'data/images/misc_animations/explosion_'))
weapon_gfx={_I:sword_0_gfx,_J:sword_1_gfx,_G:sword_2_gfx,_H:sword_3_gfx}
def gen_id(name,frame):return os.path.join(os.path.abspath(os.path.dirname(__file__)),'data/images/weapon_effects/'+name+'_'+str(frame))
tiles={_j:[_F,0,0,0],_k:[_F,0,1,0],_l:[_F,1,0,0],_m:[_F,1,1,0]}
decor={}
scroll_x=-100
scroll_y=-50
SKY=146,244,255
directions=[0,0,0,0]
dirs=[[1,0],[-1,0],[0,1],[0,-1]]
new_tile_timer=0
player=entity(0,0,20,20)
player.set_animation_tags([_T])
player.animation=player_walk_f
player_dir=_b
player_knockback=[0,0]
current_weapon=_I
attack_sizes={_I:104,_J:124,_G:140,_H:144}
attack_powers={_I:4,_J:5,_G:7,_H:7}
attack_knockbacks={_I:8,_J:12,_G:16,_H:16}
enemy_knockbacks={_D:4,_N:6,_E:14}
enemy_damages={_D:3,_N:5,_E:10}
knockback_multipliers={_D:1,_N:0.25,_E:0.125}
enemy_health={_D:10,_N:12,_E:24}
attack_timer=-1
attack_base=0
dash_timer=-1
dash_start=[0,0]
health=100
energy=50
rate_x=0.5
rate_y=0.5
last_frame=get_ms()
alerts=[]
for_render=[]
image_cache=[]
enemies=[]
enemy_types=[_D,_D,_D,_N,_D,_D,_N,_D,_D,_E]
decor_types=[_U,_U,_U,_U,_Z,_L,_L,_Z,_Z,_Q]
cloud_types=[_R,_R,_a,_R,_R,_a,_e]
particles=[]
screen_shake=0
new_game=180
hurt=0
lock_mouse=_B
time_alive=0
explosions=[]
projectiles=[]
dust=[]
paused=_B
minutes=0
remove_tiles=[]
next_enemy=_A
clouds=[]
for i in range(10):depth=random.randint(0,5)/10+0.25;clouds.append([random.choice(cloud_types),random.randint(-44,290)+scroll_x*depth,random.randint(0,200)+scroll_y*depth,depth,random.randint(4,10)/20])
inventory=[[_A,0,-30],[_A,0,-30],[_A,0,-30],[_A,0,-30]]
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.65)
def play():
	F='Press R to restart.';E='You died in ';D='Paused';C='No Energy!';B='-blueberries +energy';A='up';global screen,scroll_x,scroll_y,time_alive,weapon_rot,new_game,minutes,new_tile_timer,attack_timer,player_knockback,dash_timer,player,tiles,rate_y,rate_x,decor,current_weapon,projectiles,enemies,remove_tiles,particles,explosions,lock_mouse,dust,WINDOWWIDTH,WINDOWHEIGHT,for_render,image_cache,health,next_enemy,hurt,screen_shake,wenemy_offset,tile_z,dash_start,attack_base,weapon_gfx_img,energy,last_frame,paused,inventory,player_dir,FPS;display.fill(SKY)
	if random.randint(1,80)==1:
		depth=random.randint(0,5)/10+0.25;t=random.choice(cloud_types)
		if random.randint(1,1000)==1:t=_f
		clouds.append([t,-44+scroll_x*depth,random.randint(0,200)+scroll_y*depth,depth,random.randint(4,10)/20])
	n=0
	for cloud in clouds:
		cloud[1]+=cloud[4];display.blit(cloud_images[cloud[0]],(cloud[1]-scroll_x*cloud[3],cloud[2]-scroll_y*cloud[3]))
		if cloud[1]-scroll_x*cloud[3]>320:clouds.pop(n);n-=1
		n+=1
	if time_alive==1400:next_enemy=_E
	if new_game!=0:new_game-=1;new_tile_rate=2
	else:new_tile_rate=13
	if minutes>8:new_tile_rate=8
	if new_tile_timer>=0:new_tile_timer+=1
	if new_tile_timer>=new_tile_rate:
		keys=[]
		for key in tiles.keys():keys.append(key)
		not_placed=_C
		while not_placed:
			key=random.choice(keys);open_spots=[]
			for direction in dirs:
				x=tiles[key][1]+direction[0];y=tiles[key][2]+direction[1]
				if loc(x,y)not in tiles:open_spots.append([x,y])
			if open_spots!=[]:
				spot=random.choice(open_spots);tiles[loc(spot[0],spot[1])]=[_F,spot[0],spot[1],200]
				if random.randint(1,int((0.7/time_alive+1/2000)*5000))==1:
					if new_game==0:
						t=random.choice(enemy_types)
						if t==_E:
							if time_alive<2000:t=_D
						if next_enemy!=_A:t=next_enemy;next_enemy=_A
						enemies.append([t,entity(spot[0]*32+6,spot[1]*32+6,20,20),[0,0],enemy_health[t],0])
				elif random.randint(1,3)==1:decor[loc(spot[0],spot[1])]=[random.choice(decor_types),spot[0],spot[1]]
				not_placed=_B
		new_tile_timer=0
	player_standing=_B
	if attack_timer!=-1:
		attack_timer+=45
		if attack_timer>=900:attack_timer=-1
	while abs(player_knockback[0])+abs(player_knockback[1])>30:
		if abs(player_knockback[0])>abs(player_knockback[1]):
			while abs(player_knockback[0])>15:
				if player_knockback[1]==0:player_knockback[1]=0.1
				player_knockback[1]-=1/abs(player_knockback[0])*player_knockback[1]/abs(player_knockback[1]);player_knockback[0]=reduce(player_knockback[0],1)
		else:
			while abs(player_knockback[1])>15:
				if player_knockback[0]==0:player_knockback[0]=0.1
				player_knockback[0]-=1/abs(player_knockback[1])*player_knockback[0]/abs(player_knockback[0]);player_knockback[1]=reduce(player_knockback[1],1)
	movement=[player_knockback[0],player_knockback[1]];player_knockback[0]=reduce(player_knockback[0],0.75);player_knockback[1]=reduce(player_knockback[1],0.75);speed=3
	if dash_timer!=-1:
		dash_timer+=1
		if dash_timer==10:dash_timer=-1
		speed=18
		if current_weapon==_G:speed=24
		elif current_weapon==_H:speed=28
	pos=loc(int(round((player.x-0.5)/32,0)),int(round((player.y-0.5)/32,0)))
	try:
		if tiles[pos][0]==_c:
			speed/=3
			for item in inventory:
				if item[0]==_V:
					item[1]-=1
					if item[1]<=0:item[0]=_A
					alerts.append(['-seeds',0]);tiles[pos][0]=_F
	except KeyError:pass
	movement[1]+=rate_y*speed*1.2-rate_x*speed;movement[0]+=rate_y*speed*1.2+rate_x*speed
	if rate_y>0:player.animation=player_walk_f;player_dir=_b;player.change_frame(1)
	elif rate_y<0:player.animation=player_walk_b;player_dir=A;player.change_frame(1)
	else:
		player.animation=_A;player_standing=_C
		if player_dir==_b:player.set_image(player_stand_f)
		else:player.set_image(player_stand_b)
	if rate_x>0:player.set_flip(_B)
	elif rate_x<0:player.set_flip(_C)
	if attack_timer!=-1:
		if weapon_rot%360<90 or weapon_rot%360>270:player.set_flip(_B)
		else:player.set_flip(_C)
		if weapon_rot%360<180:player.animation=player_walk_f;player_dir=_b
		else:player.animation=player_walk_b;player_dir=A
	nearby_collidables=[];player_loc=[int(player.x/32),int(player.y/32)]
	for y in range(7):
		for x in range(7):
			pos_raw=[x+player_loc[0]-3,y+player_loc[1]-3];pos=loc(pos_raw[0],pos_raw[1])
			if pos not in tiles:nearby_collidables.append([pos_raw[0]*32,pos_raw[1]*32,32,32])
			elif tiles[pos][3]>0:nearby_collidables.append([pos_raw[0]*32,pos_raw[1]*32,32,32])
			elif pos in decor:nearby_collidables.append([pos_raw[0]*32,pos_raw[1]*32,32,32])
	movement[0]=cap(movement[0],24);movement[1]=cap(movement[1],24);player.move(movement,nearby_collidables);player_img=player.get_current_img();hit_enemy=_B;hit_decor=_B;been_hurt=_B;attackR=pygame.Rect(player.x+10-int(attack_sizes[current_weapon]/2),player.y+10-int(attack_sizes[current_weapon]/2),attack_sizes[current_weapon],attack_sizes[current_weapon]);n=0
	for projectile in projectiles:
		projectileR=pygame.Rect(projectile[0],projectile[1],20,20)
		if projectileR.colliderect(attackR):render_pos=int(projectile[0]/32*14-projectile[1]/32*14),int(projectile[0]/32*7+projectile[1]/32*7);add_img_particles(shot_img,render_pos,_B,20);projectiles.pop(n);hit_decor=_C;n-=1
		n+=1
	for enemy in enemies:
		if player.obj.rect.colliderect(enemy[1].obj.rect):
			if dash_timer==-1:
				health-=enemy_damages[enemy[0]];hurt+=enemy_damages[enemy[0]]*5;e_dis_x=enemy[1].x-player.x;e_dis_y=enemy[1].y-player.y
				if e_dis_x==0 and e_dis_y==0:e_dis_x=1;e_dis_y=1
				e_rate_x=e_dis_x/(abs(e_dis_x)+abs(e_dis_y));e_rate_y=e_dis_y/(abs(e_dis_x)+abs(e_dis_y));player_knockback[0]-=e_rate_x*enemy_knockbacks[enemy[0]]*4;player_knockback[1]-=e_rate_y*enemy_knockbacks[enemy[0]]*4;been_hurt=_C
		if attack_timer!=-1:
			if attackR.colliderect(enemy[1].obj.rect):
				if enemy[4]==0:
					try:tile_z=tiles[loc(int((enemy[1].x-6)/32),int((enemy[1].y-6)/32))][3]
					except KeyError:tile_z=0
					if tile_z==0:
						enemy[4]=10;enemy[3]-=attack_powers[current_weapon];e_dis_x=enemy[1].x-player.x;e_dis_y=enemy[1].y-player.y
						if e_dis_x==0 and e_dis_y==0:e_dis_x=1;e_dis_y=1
						e_rate_x=e_dis_x/(abs(e_dis_x)+abs(e_dis_y));e_rate_y=e_dis_y/(abs(e_dis_x)+abs(e_dis_y));enemy[2][0]+=e_rate_x*attack_knockbacks[current_weapon]*knockback_multipliers[enemy[0]];enemy[2][1]+=e_rate_y*attack_knockbacks[current_weapon]*knockback_multipliers[enemy[0]];screen_shake+=int(enemy_knockbacks[enemy[0]]);player_knockback[0]-=e_rate_x*enemy_knockbacks[enemy[0]];player_knockback[1]-=e_rate_y*enemy_knockbacks[enemy[0]];hit_enemy=_C
	if hit_enemy:hit_s.play()
	if been_hurt:hurt_s.play()
	n=0
	for tile in remove_tiles:
		try:
			if tiles[tile][3]==0:tiles[tile][3]=1
			tiles[tile][3]-=(0-tiles[tile][3])/10
		except KeyError:remove_tiles.pop(n);n-=1
		n+=1
	temp_scroll_x=scroll_x+5;temp_scroll_y=scroll_y-93;start_pos=[int(temp_scroll_x/28)+int(temp_scroll_y/14)+4,int(temp_scroll_y/14)-int(temp_scroll_x/28)-4];render_box_size=30;render_box={};remove_list=[]
	for y in range(render_box_size):
		for x in range(render_box_size):
			try:
				key=loc(x+start_pos[0],y+start_pos[1]);render_box[key]=tiles[key].copy()
				if tiles[key][3]>0:
					if key not in remove_tiles:tiles[key][3]-=tiles[key][3]/10
					if tiles[key][3]<1:tiles[key][3]=0
					if tiles[key][3]>250:remove_list.append(key)
			except KeyError:pass
	for i in range(render_box_size*2-1):
		for i2 in range(render_box_size):
			pos=[i-i2,i2]
			try:tile=render_box[loc(pos[0]+start_pos[0],pos[1]+start_pos[1])];display.blit(tile_images[tile[0]],(tile[1]*14-tile[2]*14-int(scroll_x),tile[1]*7+tile[2]*7-int(scroll_y)+int(tile[3])))
			except KeyError:pass
	for tile in remove_list:
		del tiles[tile]
		if tile in render_box:del render_box[tile]
	remove_list=[]
	for obj in decor:
		x=decor[obj][1];y=decor[obj][2]
		try:z=render_box[obj][3]
		except KeyError:z=-1
		if z!=-1:
			render_pos=int(x*14-y*14)-scroll_x,int(x*7+y*7)+decor_images[decor[obj][0]][1]-scroll_y-z;ordered_render(decor_images[decor[obj][0]][0],render_pos);objR=pygame.Rect(x*32,y*32,32,32)
			if attack_timer!=-1:
				if attackR.colliderect(objR):
					if tiles[obj][3]==0:
						if decor[obj][0]==_L:add_item(_L);alerts.append(['+blueberries',0])
						if decor[obj][0]==_Q:add_item(_Q);alerts.append(['+apples',0])
						if random.randint(1,8)==1:
							if current_weapon==_H:
								for i in range(6):add_item(_V)
								alerts.append(['+6 seeds',0])
							elif current_weapon==_G:
								for i in range(4):add_item(_V)
								alerts.append(['+4 seeds',0])
							else:
								for i in range(2):add_item(_V)
								alerts.append(['+2 seeds',0])
						add_img_particles(decor_images[decor[obj][0]][0],(render_pos[0]+scroll_x,render_pos[1]+scroll_y),_B,20);remove_list.append(obj);hit_decor=_C
	for obj in remove_list:del decor[obj]
	if hit_decor:hit_decor_s.play()
	n=0
	for particle in particles:
		display.set_at((int(particle[1]-scroll_x),int(particle[2]-scroll_y)),particle[0]);particle[1]+=particle[3];particle[2]+=particle[4];particle[5]-=1
		if particle[5]<25:
			if particle[3]==0 and particle[4]==0:particle[3]=random.randint(0,20)/10-1;particle[4]=random.randint(0,20)/10-1
		if particle[5]<=0:particles.pop(n);n-=1
		n+=1
	n=0
	for explosion in explosions:
		if explosion[1]==0:explosion[0].set_animation(explosion_anim)
		explosion_img=explosion[0].get_current_img();render_pos=int(explosion[0].x/32*14-explosion[0].y/32*14)-scroll_x,int(explosion[0].x/32*7+explosion[0].y/32*7)-17-scroll_y;ordered_render(explosion_img,render_pos);explosion[0].change_frame(1);explosion[1]+=1
		if explosion[1]==16:
			try:pos=loc(int(explosion[0].x/32),int(explosion[0].y/32));tiles[pos][0]=_c
			except KeyError:pass
		if explosion[1]==38:explosion_s.play()
		if explosion[1]==42:
			if explosion[0].obj.rect.colliderect(player.obj.rect):
				e_dis_x=explosion[0].x-player.x;e_dis_y=explosion[0].y-player.y
				if e_dis_x==0 and e_dis_y==0:e_dis_x=1;e_dis_y=1
				e_rate_x=e_dis_x/(abs(e_dis_x)+abs(e_dis_y));e_rate_y=e_dis_y/(abs(e_dis_x)+abs(e_dis_y));player_knockback[0]-=e_rate_x*12;player_knockback[1]-=e_rate_y*12;health-=15;hurt+=15*5
		if explosion[1]==66:explosions.pop(n);n-=1
		n+=1
	n=0
	for enemy in enemies:
		enemy_img=_A;enemy_movement=[enemy[2][0],enemy[2][1]];enemy[2][0]=reduce(enemy[2][0],0.5);enemy[2][1]=reduce(enemy[2][1],0.5)
		if enemy[4]>0:enemy[4]-=1
		if enemy[0]in[_D,_E]:
			if len(enemy)==5:
				enemy.append(0);enemy.append([_K,_B])
				if enemy[0]==_E:enemy[1].set_animation_tags([_T])
			try:tile_z=render_box[loc(int((enemy[1].x-6)/32),int((enemy[1].y-6)/32))][3]
			except KeyError:
				if loc(int((enemy[1].x-6)/32),int((enemy[1].y-6)/32))in tiles:tile_z=-1
				else:tile_z=0
			if enemy[0]==_D:enemy_img=fly_stand_f.copy();enemy_offset=[7,-7-tile_z]
			if enemy[0]==_E:enemy_offset=[0,-14-tile_z];enemy[1].animation=tank_main_f;enemy_img=enemy[1].get_current_img()
			if tile_z==0:enemy[5]+=1
			if enemy[5]==30:enemy[5]=0-random.randint(15,35)
			if(enemy[5]<0 or enemy[0]==_E)and tile_z==0:
				e_dis_x=player.x-enemy[1].x;e_dis_y=player.y-enemy[1].y
				if e_dis_x==0 and e_dis_y==0:e_dis_x=1;e_dis_y=1
				e_rate_x=e_dis_x/(abs(e_dis_x)+abs(e_dis_y));e_rate_y=e_dis_y/(abs(e_dis_x)+abs(e_dis_y))
				if enemy[0]==_D:speed=5
				if enemy[0]==_E:speed=1.5
				enemy_movement[0]+=e_rate_x*speed;enemy_movement[1]+=e_rate_y*speed*1.2
				if e_rate_x>e_rate_y*1.2:
					if e_rate_x>0:enemy[6][1]=_B;enemy[6][0]=_K
					elif e_rate_x<0:enemy[6][1]=_B;enemy[6][0]=_M
				elif e_rate_y>0:enemy[6][1]=_C;enemy[6][0]=_K
				elif e_rate_y<0:enemy[6][1]=_C;enemy[6][0]=_M
				if enemy[0]==_D:
					if enemy[6][0]==_K:enemy_img=flip(fly_fly_f,enemy[6][1]).copy()
					if enemy[6][0]==_M:enemy_img=flip(fly_fly_b,enemy[6][1]).copy()
				elif enemy[0]==_E:
					if enemy[1].animation_frame==132:
						if len(projectiles)<40:projectiles.append([enemy[1].x+5,enemy[1].y-5,e_rate_x,e_rate_y,0])
						damageR=pygame.Rect(enemy[1].x+14-32,enemy[1].y+11-32,64,64)
						if damageR.colliderect(player):
							health-=5;hurt+=25;e_dis_x=enemy[1].x-player.x;e_dis_y=enemy[1].y-player.y
							if e_dis_x==0 and e_dis_y==0:e_dis_x=1;e_dis_y=1
							e_rate_x=e_dis_x/(abs(e_dis_x)+abs(e_dis_y));e_rate_y=e_dis_y/(abs(e_dis_x)+abs(e_dis_y));player_knockback[0]-=e_rate_x*enemy_knockbacks[enemy[0]]*8;player_knockback[1]-=e_rate_y*enemy_knockbacks[enemy[0]]*8
					if enemy[6][0]==_K:enemy[1].animation=tank_main_f
					if enemy[6][0]==_M:enemy[1].animation=tank_main_b
					enemy[1].change_frame(1);enemy_img=enemy[1].get_current_img()
			elif enemy[0]==_D:
				if enemy[6][0]==_K:enemy_img=flip(fly_stand_f,enemy[6][1]).copy()
				if enemy[6][0]==_M:enemy_img=flip(fly_stand_b,enemy[6][1]).copy()
		if enemy[0]==_N:
			if len(enemy)==5:enemy[1].animation=stomper_stomp;enemy[1].set_animation_tags([_T])
			enemy_img=enemy[1].get_current_img();enemy[1].change_frame(1)
			try:tile_z=render_box[loc(int((enemy[1].x-6)/32),int((enemy[1].y-6)/32))][3]
			except KeyError:
				if loc(int((enemy[1].x-6)/32),int((enemy[1].y-6)/32))in tiles:tile_z=-1
				else:tile_z=0
			if enemy[1].animation_frame==86:
				for attampt in range(10):
					try:
						pos_raw=[int(player.x/32)+random.randint(0,3)-1,int(player.y/32)+random.randint(0,3)-1];pos=loc(pos_raw[0],pos_raw[1])
						if tiles[pos][0]==_F:
							if tiles[pos][3]==0:explosions.append([entity(pos_raw[0]*32,pos_raw[1]*32,32,32),0]);break
					except KeyError:pass
			enemy_offset=[5,-15-tile_z]
		if enemy[4]>0:
			if enemy[3]>0:red_surf=pygame.Surface((enemy_img.get_width(),enemy_img.get_height()));red_surf.fill((100,0,0));red_surf.set_alpha(400-enemy[4]*20);enemy_img.blit(red_surf,(0,0),special_flags=BLEND_ADD)
		enemy[1].move(enemy_movement,get_nearby_tiles((enemy[1].x,enemy[1].y),tiles));render_pos=int(enemy[1].x/32*14-enemy[1].y/32*14)+enemy_offset[0]-scroll_x,int(enemy[1].x/32*7+enemy[1].y/32*7)+enemy_offset[1]-scroll_y
		if enemy[0]==_E:
			if tile_z==0:
				if random.randint(1,3)==1:dust.append([entity(render_pos[0]+scroll_x+14,render_pos[1]+scroll_y+22,2,2),random.randint(0,20)/20-0.5,random.randint(0,20)/20-0.5,0])
		if enemy[3]<=0:
			if enemy[0]==_D:
				tile_str=str(int(round(enemy[1].x/32,0)))+_Y+str(int(round(enemy[1].y/32,0)))
				if tile_str in tiles:
					if tile_str not in decor:
						tileR=pygame.Rect(tiles[tile_str][1]*32,tiles[tile_str][2]*32,32,32);collided=_B
						for projectile in projectiles:
							projectileR=pygame.Rect(projectile[0],projectile[1],20,20)
							if projectileR.colliderect(tileR):collided=_C
						n2=0
						for enemy2 in enemies:
							enemyR=pygame.Rect(enemy2[1].x-10,enemy2[1].y-10,40,40)
							if enemyR.colliderect(tileR):
								if n!=n2:collided=_C
							n2+=1
						if player.obj.rect.colliderect(tileR):collided=_C
						if collided==_B:remove_tiles.append(tile_str)
			add_item(_d);alerts.append(['+gel',0]);enemies.pop(n);add_img_particles(enemy_img,(render_pos[0]+scroll_x,render_pos[1]+scroll_y));n-=1
		if enemy_img!=_A:
			if tile_z!=-1:ordered_render(enemy_img,render_pos)
		n+=1
	weapon_img=weapons[current_weapon];x=player.x;y=player.y;render_x=int(x/32*14-y/32*14)+9;render_y=int(x/32*7+y/32*7)-12
	if player_standing==_B:
		if random.randint(1,5)==1:dust.append([entity(render_x+4,render_y+18,2,2),random.randint(0,20)/20-0.5,random.randint(0,20)/20-0.5,0])
	MX,MY=pygame.mouse.get_pos()
	if lock_mouse==_C:
		if MX<10:pygame.mouse.set_pos(10,MY)
		if MX>WINDOWWIDTH-10:pygame.mouse.set_pos(WINDOWWIDTH-10,MY)
		if MY<10:pygame.mouse.set_pos(MX,10)
		if MY>WINDOWHEIGHT-10:pygame.mouse.set_pos(MX,WINDOWHEIGHT-10)
	MX/=WINDOWWIDTH;MY/=WINDOWHEIGHT;dis_x=MX-(render_x+4-scroll_x)/300;dis_y=MY-(render_y+5-scroll_y)/200
	if abs(dis_x)+abs(dis_y)<0.075:rate_x=0;rate_y=0
	else:rate_x=dis_x/(abs(dis_x)+abs(dis_y));rate_y=dis_y/(abs(dis_x)+abs(dis_y))
	if dash_timer!=-1:
		y=dash_start[1]-render_y;x=dash_start[0]-render_x
		if x==0 and y==0:x=1;y=1
		slope=[x/(abs(x)+abs(y)),y/(abs(x)+abs(y))];perp_slope=[-slope[1],slope[0]];perp_slope2=[slope[1],-slope[0]];d=10-dash_timer;points=[[dash_start[0]-scroll_x,dash_start[1]-scroll_y],[render_x+4-scroll_x+perp_slope[0]*d,render_y+18-scroll_y+perp_slope[1]*d],[render_x+4-scroll_x-int(x/2),render_y+18-scroll_y-int(y/2)],[render_x+4-scroll_x+perp_slope2[0]*d,render_y+18-scroll_y+perp_slope2[1]*d]];pygame.draw.polygon(display,(169,59,59),points)
	weapon_rot=point_degrees(((render_x-scroll_x)/300,(render_y-scroll_y)/200),(MX,MY))
	if attack_timer!=-1:
		weapon_rot=attack_timer
		if weapon_rot>720:weapon_rot=720
		weapon_rot+=attack_base;weapon_gfx_img=pygame.transform.rotate(get_frame(gen_id(current_weapon,int(attack_timer/45))).copy(),attack_base)
	weapon_img=pygame.transform.rotate(weapon_img,-weapon_rot)
	if weapon_rot<0:weapon_rot+=360
	if attack_timer!=-1:display.blit(weapon_gfx_img,(render_x-scroll_x-int(weapon_gfx_img.get_width()/2)+3,render_y-scroll_y-int(weapon_gfx_img.get_height()/2)+9))
	z=-1
	if weapon_rot%360<180:z=1
	ordered_render(weapon_img,(render_x-scroll_x-int(weapon_img.get_width()/2)+3,render_y-scroll_y-int(weapon_img.get_height()/2)+9),render_y-scroll_y+player_img.get_height(),z);ordered_render(player_img,(render_x-scroll_x,render_y-scroll_y));scroll_x+=(render_x-150-scroll_x)/20;scroll_y+=(render_y-100-scroll_y)/20;for_render.sort()
	for img in for_render:display.blit(image_cache[img[4]],(img[2],img[3]))
	for_render=[];image_cache=[];n=0
	for particle in dust:
		particle[0].x+=particle[1];particle[0].y+=particle[2]
		if particle[0].animation is _A:particle[0].animation=dust_anim
		ordered_render(particle[0].get_current_img().copy(),(particle[0].x-scroll_x,particle[0].y-scroll_y));particle[0].change_frame(1);particle[3]+=1
		if particle[3]>=31:dust.pop(n);n-=1
		n+=1
	for projectile in projectiles:
		obj=PhysicsObject(projectile[0],projectile[1],20,20);collisions=obj.move([projectile[2]*3,projectile[3]*3],get_nearby_tiles((obj.x,obj.y),tiles))
		for c in collisions:
			if collisions[c]==_C:projectile[2]*=-1;projectile[3]*=-1
		projectile[0]=obj.x;projectile[1]=obj.y;projectile[4]+=1;render_pos=int(projectile[0]/32*14-projectile[1]/32*14)-scroll_x,int(projectile[0]/32*7+projectile[1]/32*7)-scroll_y;display.blit(shot_img,render_pos)
		if obj.rect.colliderect(player.obj.rect):
			projectile[2]*=-1;projectile[3]*=-1;e_dis_x=obj.x-player.x;e_dis_y=obj.y-player.y
			if e_dis_x==0 and e_dis_y==0:e_dis_x=1;e_dis_y=1
			e_rate_x=e_dis_x/(abs(e_dis_x)+abs(e_dis_y));e_rate_y=e_dis_y/(abs(e_dis_x)+abs(e_dis_y));player_knockback[0]-=e_rate_x*4;player_knockback[1]-=e_rate_y*4;health-=2;hurt+=10
	n=0
	for alert in alerts:
		alert_w=get_text_width(alert[0],1);alert_surf=pygame.Surface((alert_w,8));show_text(alert[0],0,0,1,99999,font_1,alert_surf);alert_surf.set_colorkey((0,0,0));alert_surf.set_alpha(510-alert[1]*51);display.blit(alert_surf,(render_x-scroll_x+4-int(alert_w/2),render_y-scroll_y-10-int(alert[1])));alert[1]+=0.2
		if alert[1]>10:alerts.pop(n);n-=1
		n+=1
	display.blit(bars_img,(0,0))
	if health>0:health_bar=pygame.Surface((int(health)+1,3));health_bar.fill((169,59,59));pygame.draw.line(health_bar,(16,30,41),(int(health),0),(int(health),3));display.blit(health_bar,(5,5))
	if energy>0:energy_bar=pygame.Surface((int(energy)+1,3));energy_bar.fill((63,199,120));pygame.draw.line(energy_bar,(16,30,41),(int(energy),0),(int(energy),3));display.blit(energy_bar,(5,12))
	energy+=0.45
	if current_weapon==_J:energy+=0.15
	elif current_weapon==_G:energy+=0.3
	elif current_weapon==_H:energy+=0.35
	if energy>50:energy=50
	minutes=int(time_alive/(40*60));seconds=int((time_alive-minutes*(40*60))/40);milliseconds=int((time_alive-minutes*(40*60)-seconds*40)*2.5);time_str=str(minutes)+_X+str(seconds)+_X+str(milliseconds);show_text(time_str,300-get_text_width(time_str,1)-1,1,1,99999,font_0,display);y=30
	for slot in inventory:
		if slot[0]is _A:slot[2]+=(-30-slot[2])/5
		else:
			slot[2]+=(1-slot[2])/5
			if 1-slot[2]<1:slot[2]=1
		display.blit(slot_img,(int(slot[2]),y))
		if slot[0]!=_A:display.blit(item_images[slot[0]],(int(slot[2])+4,y+4))
		if slot[0]==_Q:
			if health<80:
				health+=20;slot[1]-=1
				if slot[1]<=0:slot[0]=_A;slot[1]=0
				alerts.append(['-apples +health',0])
		if slot[0]==_d:
			if current_weapon==_I:
				if slot[1]>=60:
					current_weapon=_J;slot[1]-=60;alerts.append(['-60 gel +sword',0])
					if slot[1]==0:slot[0]=_A
			if current_weapon==_J:
				if slot[1]>=150:
					current_weapon=_G;slot[1]-=150;alerts.append(['-150 gel +sword',0])
					if slot[1]==0:slot[0]=_A
			if current_weapon==_G:
				if slot[1]>=300:
					current_weapon=_H;slot[1]-=300;alerts.append(['-300 gel +sword',0])
					if slot[1]==0:slot[0]=_A
		show_text(str(slot[1]),int(slot[2])+19-get_text_width(str(slot[1]),1),y+13,1,99999,font_1,display);y+=25
	display.blit(weapon_slot,(1,177));display.blit(weapon_items[current_weapon],(5,182))
	if new_game>0:controls_img.set_alpha(new_game*4);display.blit(controls_img,(112,30))
	for event in pygame.event.get():
		if event.type==QUIT:pygame.quit();sys.exit()
		if event.type==KEYDOWN:
			if event.key==K_ESCAPE:pygame.quit();sys.exit()
			if event.key==K_UP:directions[0]=_C
			if event.key==K_RIGHT:directions[1]=_C
			if event.key==K_DOWN:directions[2]=_C
			if event.key==K_LEFT:directions[3]=_C
			if event.key==K_m:
				if lock_mouse==_B:lock_mouse=_C
				else:lock_mouse=_B
			if event.key==K_p:paused=_C
			if event.key==K_F11:
				if WINDOWWIDTH==600:WINDOWWIDTH=900;WINDOWHEIGHT=600
				else:WINDOWWIDTH=600;WINDOWHEIGHT=400
				screen=pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT),0,32)
		if event.type==KEYUP:
			if event.key==K_UP:directions[0]=_B
			if event.key==K_RIGHT:directions[1]=_B
			if event.key==K_DOWN:directions[2]=_B
			if event.key==K_LEFT:directions[3]=_B
		if event.type==MOUSEBUTTONDOWN:
			if event.button==1:
				if attack_timer==-1:
					if energy>15:energy-=15;attack_timer=0;attack_base=weapon_rot;attack_s.play()
					else:
						for item in inventory:
							if item[0]==_L:
								item[1]-=1
								if item[1]==0:item[0]=_A
								energy+=50;alerts.append([B,0])
						if energy>15:energy-=15;attack_timer=0;attack_base=weapon_rot;attack_s.play()
						else:alerts.append([C,0])
			if event.button==3:
				if dash_timer==-1:
					if energy>10:energy-=10;dash_timer=0;dash_start=[render_x+4,render_y+18];dash_s.play()
					else:
						for item in inventory:
							if item[0]==_L:
								item[1]-=1
								if item[1]==0:item[0]=_A
								energy+=50;alerts.append([B,0])
						if energy>10:energy-=10;dash_timer=0;dash_start=[render_x+4,render_y+18];dash_s.play()
						else:alerts.append([C,0])
	time_alive+=1
	if hurt>0:
		hurt-=1;hurt_surf=pygame.Surface((300,200));hurt_surf.fill((169,59,59));hurt_surf.set_alpha(cap(hurt*4,180))
		if hurt>60:hurt=60
		display.blit(hurt_surf,(0,0))
	frame_ms=get_ms()-last_frame;last_frame=get_ms();FPS=int(1000/frame_ms)
	while paused:
		screen_shake=0;show_text(D,150-int(get_text_width(D,1)/2),96,1,99999,font_1,display)
		for event in pygame.event.get():
			if event.type==QUIT:pygame.quit();sys.exit()
			if event.type==KEYDOWN:
				if event.key==K_ESCAPE:pygame.quit();sys.exit()
				if event.key==K_p:paused=_B
				if event.key==K_F11:
					if WINDOWWIDTH==600:WINDOWWIDTH=900;WINDOWHEIGHT=600
					else:WINDOWWIDTH=600;WINDOWHEIGHT=400
					screen=pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT),0,32)
		screen.blit(pygame.transform.scale(display,(WINDOWWIDTH,WINDOWHEIGHT)),(random.randint(0,cap(int(screen_shake),5)*2)-int(screen_shake),random.randint(0,cap(int(screen_shake),5)*2)-int(screen_shake)));pygame.display.update();mainClock.tick(40)
	while health<=0:
		screen_shake=0;show_text(E+time_str+_W,150-int(get_text_width(E+time_str+_W,1)/2),90,1,99999,font_1,display);show_text(F,150-int(get_text_width(F,1)/2),100,1,99999,font_1,display)
		for event in pygame.event.get():
			if event.type==QUIT:pygame.quit();sys.exit()
			if event.type==KEYDOWN:
				if event.key==K_ESCAPE:pygame.quit();sys.exit()
				if event.key==K_F11:
					if WINDOWWIDTH==600:WINDOWWIDTH=900;WINDOWHEIGHT=600
					else:WINDOWWIDTH=600;WINDOWHEIGHT=400
					screen=pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT),0,32)
				if event.key==K_r:health=100;energy=50;attack_timer=-1;dash_timer=-1;enemies=[];tiles={_j:[_F,0,0,0],_k:[_F,0,1,0],_l:[_F,1,0,0],_m:[_F,1,1,0]};scroll_x=-100;scroll_y=-50;player=entity(0,0,20,20);new_game=180;current_weapon=_I;player_knockback=[0,0];hurt=0;new_tile_timer=0;particles=[];time_alive=1;explosions=[];inventory=[[_A,0,-30],[_A,0,-30],[_A,0,-30],[_A,0,-30]];decor={};dust=[];projectiles=[];remove_tiles=[];next_enemy=_A
		screen.blit(pygame.transform.scale(display,(WINDOWWIDTH,WINDOWHEIGHT)),(random.randint(0,cap(int(screen_shake),5)*2)-int(screen_shake),random.randint(0,cap(int(screen_shake),5)*2)-int(screen_shake)));pygame.display.update();mainClock.tick(40)
	screen.blit(pygame.transform.scale(display,(WINDOWWIDTH,WINDOWHEIGHT)),(random.randint(0,cap(int(screen_shake),5)*2)-int(screen_shake),random.randint(0,cap(int(screen_shake),5)*2)-int(screen_shake)))
	if screen_shake>0:screen_shake-=0.5
	if screen_shake>10:screen_shake=10
	pygame.display.update();mainClock.tick(40)
def main():
	while _C:play()
