import pygame
import os
from music import Music
from scene import Scene
import random
from gameover import GameOverScene
import time

random_data =os.urandom(4)
seed = int.from_bytes(random_data, byteorder='big')
random.seed(seed)

BG_COLOR = (0,0,0)
anecdots = ['Говорит новый русский знакомому сталкеру: — Эта, слыш (деловито)… зэлатую рыпку мине падгани. Бабла кину — скока скажешь… А то у пацанов всех, внатуре, есть, а я один вроде лох получается (недоумевает). Ну. Сталкер обалдел: — Так этаж, этаж ведь… артефакт (приходит в себя) такой радиоактивный. Новый русский: — Не, ну хэре гнать (деловито). Артефакт, шмартефакт, я ж его не в трусы положу (успокаивает). Ййя ккак палагается, на цепуру желтявую, шооб фсе как у людэй. ','Заблудился как-то долговец и кричит: — Люди (протяжно), отзовитесь, кто нибудь ыууу. Тут его кто то догоняет и… хлоп сзади по рюкзаку. Ну он оборачивается, а там стоит кровосос. Грустный такой. И хлюпает ему: — Щево арешь, а? У долговца уже полные штаны ежиков… но он все-таки отвечает: — Я тово (нервничает), запплутал. Кричу, вот может кто-нибудь услышит (неуверенно)? Кровосос помолчал, помолчал и говорит ему: — Ну я вот услышал (очень недовольно) и чево теперь делать будем?', 'Сидят два сталкера на берегу озера. Один другому говорит: — Насчет радиации я тебе чего скажу (со знанием дела). Гонят как не знаю кто (улыбается)! Я тут уже лет 5 шарюсь безвылазно. Изменений никаких не заметил (с восхищением)! Сам как думаешь (неуверенно)? — Да фигня однозначно (томным голосом). Хотя (задумался)… С другой стороны (кряхтя), чешуя-то в последнее время чешется все чаще.', 'Встречаются двое сталкеров ну и один говорит: — На днях к Долгу заходил… — Ну и? (вопрошает) — Чо и? (недовольный) И остался должен. Ха. А потом зашел к Свободе… — Ну и чо? — И стал СВОБОДЕН!', 'Студент на экзамене: — Профессор, понимаете (томным голосом), я не могу сдать математику… потому что совсем не сплю в последний месяц. Вот только закрою глаза как появляется страшная картина… меня прижали к стене атомной станци и какие-то страшные мутанты и готовы разорвать… в клочки. А профессор говорит: — Ха (злая ухмылка). Окончив институт с теперешними знаниями, молодой человек, наверняка, вы подались бы в сталкеры… а там и до ужаса, который вы увидели, совсем недалеко (читает нотацию). Да (улыбается), н о у меня есть верное средство. Поскольку переэкзаменовка по математике так и не сдана, то (строго) вы будете отчислены и пойдете служить. И никаких монстров (радостно), кроме, разве что, «дедов». ' ,'Объявление в Баре. " …По поводу празднования дня сталкера организуется выход в глубину зоны для охоты, — в скобках: монстры, — собирательство — в скобках: артефакты. Сбор всех любителей этого дела назначен на 6.30. «Этого дела» брать по два литра. " ', 'Бродит, говорят, по зоне ходячая аномалия — непьющий и некурящий сталкер. «Приманивается на запах молочка или манной каши. Способ дистанционного обнаружения — на расстоянии 200 метров от объекта… счетчик Гейгера зашкаливает.»', 'Допрашивает как-то «погонник» опытного сталкерюгу: — То есть вы признаете (официальным тоном), что в нетрезвом виде пытались покинуть территорию Зоны, в районе 12-го блок-поста и имели при себе запрещенные к выносу за ее пределы предметы (вопрошает)? Ну того запарило третий час под конвоем сидеть… Он и ему говорит: — Так… я! Признаю, командир (почти крича)! Все признаю — вот те крест! Был бы трезвый — (недовольно скалится и выделяя каждое слово) я бы в жизни, мимо вас, уродов, с хабаром бы не поперся. ']

def blit_text(surface, text, pos, font, color=pygame.Color('white')):
    words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
    space = font.size(' ')[0]  # The width of a space.
    max_width, max_height = surface.get_size()
    x, y = pos
    for line in words:
        for word in line:
            word_surface = font.render(word, 0, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = pos[0]  # Reset the x.
                y += word_height  # Start on new row.
            surface.blit(word_surface, (x, y))
            x += word_width + space
        x = pos[0]  # Reset the x.
        y += word_height  # Start on new row.

class Engine():

    def __init__(self):
        os.environ["SDL_VIDEO_CENTERED"] = "1"
        pygame.init()

        pygame.display.set_caption("S.T.A.L.K.E.R 2. Тень Даммаска")
        self.bg_image = pygame.image.load('bg.jpg')
        self.screen = pygame.display.set_mode((1280,1024))
        self.bg_image = pygame.transform.scale(self.bg_image, (1280,1024))
        self.clock = pygame.time.Clock()
        self.player = Music()
        self.start_time = time.time()
        self.events = []

        self.newGame()

    def loop(self):
        pygame.mixer.music.load('ost/stalker.wav')
        pygame.mixer.music.play(-1)
        self.song_lib_game = self.player.shuffle_lib('game')
        self.song_lib_crash = self.player.shuffle_lib('crash')
        self.song_lib_win = self.player.shuffle_lib('win')
        last_time = self.clock.get_time()
        dt_music = 5001
        dt_anec = 15001
        n_of_anecdote = 0
        self.screen.blit(self.bg_image,[0,0])
        font = pygame.font.Font(None,25)
        font_big = pygame.font.Font(None, 100)

        while True:
            self.__getEvents()
            dt_music += last_time - self.clock.get_time()
            dt_anec += last_time - self.clock.get_time()



            self.time = time.time() - self.start_time
            self.screen.blit(self.bg_image,[0,0])
            res_str = "Время прохождения: " + str(self.time) + "\n Кол-во шагов: " + str(self.scene.npc.moves) + "\n"

            blit_text(self.screen, res_str, (500,200), font)
            blit_text(self.screen, "ANECDOTI(poka proxoidsh igru)", (500,300),font_big)
            blit_text(self.screen, anecdots[n_of_anecdote], (500,500),font)

            if(abs(dt_anec) > 15000):

                dt_anec = 0
                if(n_of_anecdote >= len(anecdots)):
                    n_of_anecdote = 0
                n_of_anecdote += 1
            if(abs(dt_music) > 5000):
                dt_music = 0
                pygame.mixer.Sound("ost/" + random.choice(self.song_lib_game)).play()


            self.clock.tick(60)


            self.scene.update()
            self.scene.render()

            pygame.display.flip()

            if self.__Quit():
                break

    def newGame(self):
        self.scene = Scene(self)

    def gameOver(self):
        self.start_time = time.time()
        self.screen.blit(self.bg_image,[0,0])
        self.scene = GameOverScene(self)

    def __Quit(self):
        for e in self.events:
            if e.type == pygame.QUIT:
                return True
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                return True
        return False

    def __getEvents(self):
        self.events = pygame.event.get()

if __name__=="__main__":
    game = Engine()
    game.loop()
    pygame.quit()
