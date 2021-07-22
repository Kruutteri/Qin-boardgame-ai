import pygame,random,keyboard,time,copy

pygame.init()
win = pygame.display.set_mode((980,780))

flip_kuva = pygame.image.load("flip.png")
flip_kuva = pygame.transform.scale(flip_kuva, (80, 80))
#0 = tyhjä
#1 = musta kylä
#2 = punainen laatta
#3 = keltainen laatta
#4 = sininen laatta

lauta = [[1,0,0,0,0,0,0,0,0,0,0,0,1],
		[0,0,0,0,0,0,0,0,0,0,0,0,0],
		[0,0,0,0,1,1,0,0,0,1,0,0,0],
		[0,0,0,0,0,0,0,0,0,0,0,0,0],
		[1,0,0,0,0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0,0,0,0,1],
		[0,0,0,0,2,0,3,0,4,0,0,0,1],
		[0,0,0,0,0,0,0,0,0,0,0,0,0],
		[0,1,0,0,0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0,1,0,0,0],
		[0,0,0,0,0,1,0,0,0,0,0,0,0],
		[0,0,0,0,0,1,0,0,0,0,0,0,0],
		[1,1,0,0,0,0,0,0,0,0,0,0,1]]

#omistuslaudalla 0 tarkoittaa, että AI omistaa alueen ja 1, että pelaaja omistaa alueen, 2, että aluetta ei omista kukaan
omistuslauta = []
for i in range(13):
	omistuslauta.append([2,2,2,2,2,2,2,2,2,2,2,2,2])

villagelauta = []
for i in range(13):
	villagelauta.append([2,2,2,2,2,2,2,2,2,2,2,2,2])

pakka = []
new = True

#22 tupla punainen laatta
#33 tupla keltainen laatta
#44 tupla sininen laatta
#23 punakeltalaatta
#24 punasinilaatta
#34 keltasinilaatta

for i in range(12):
	pakka.append(22)
	pakka.append(33)
	pakka.append(44)
	pakka.append(23)
	pakka.append(24)
	pakka.append(34)

palanen = None
p_hand = []
for i in range(3):
	kortti = random.choice(pakka)
	p_hand.append(kortti)
	pakka.remove(kortti)

ai_hand = []
for i in range(3):
	kortti = random.choice(pakka)
	ai_hand.append(kortti)
	pakka.remove(kortti)

ai_hand = [22,22,23]

#optimoidaan ai nopeutta laittamalla se käymään ensin kaikki tuplat jotka sillä on kädessä
ai_hand_temp = []
for pala in ai_hand:
	if pala==22 or pala==33 or pala==44:
		ai_hand.remove(pala)
		ai_hand_temp.append(pala)

for pala in ai_hand:
	ai_hand_temp.append(pala)

ai_hand = copy.deepcopy(ai_hand_temp)

#ai_hand_2 = []
#for i in range(3):
#	kortti = random.choice(pakka)
#	ai_hand_2.append(kortti)
#	pakka.remove(kortti)


vuoro = 0

#ai_hand = [22,22,22]
#p_hand = [33,33,22]

#pisteet menevät listalla vuoron mukaan, esim jos vuoro on 1, niin pisteet[1] ovat kyseisellä vuorolla pelaavan pisteet
#eli pisteet[vuoro] keinolla pystyy käsittelemään kyseisellä vuorolla pelaavan pisteitä
printtaile = False

pisteet = [0,0]

villagepisteet_ai = 0
villagepisteet_pelaaja = 0

suunta = 1
valittu_1 = False
valittu_2 = False
valittu_3 = False

def display(omistuslauta,lauta):
	global p_hand,valittu_1,valittu_2,valittu_3,suunta,pisteet
	pygame.event.get()

	#win.fill((200,200,200))

	for i in range(14):
		pygame.draw.line(win,(255,255,255),(0,i*60),(780,i*60),2)
		pygame.draw.line(win,(255,255,255),(i*60,0),(i*60,780),2)

	for i in range(len(lauta)):
		for j in range(len(lauta)):

			if lauta[i][j] == 1:
				pygame.draw.rect(win,(0,0,0),(j*60, i*60, 60, 60))

			elif lauta[i][j] == 2:
				pygame.draw.rect(win,(255,0,0),(j*60, i*60, 60, 60))

			elif lauta[i][j] == 3:
				pygame.draw.rect(win,(255,255,0),(j*60, i*60, 60, 60))

			elif lauta[i][j] == 4:
				pygame.draw.rect(win,(0,0,255),(j*60, i*60, 60, 60))

	a = 1
	for i in range(3):
		if p_hand[i] == 22:
			pygame.draw.rect(win,(255,0,0),(820, a*150, 120 ,60))

		elif p_hand[i] == 33:
			pygame.draw.rect(win,(255,255,0),(820, a*150, 120 ,60))

		elif p_hand[i] == 44:
			pygame.draw.rect(win,(0,0,255),(820, a*150, 120 ,60))

		elif p_hand[i] == 23:
			pygame.draw.rect(win,(255,0,0),(820, a*150, 60 ,60))
			pygame.draw.rect(win,(255,255,0),(820+60, a*150, 60 ,60))

		elif p_hand[i] == 24:
			pygame.draw.rect(win,(255,0,0),(820, a*150, 60 ,60))
			pygame.draw.rect(win,(0,0,255),(820+60, a*150, 60 ,60))

		elif p_hand[i] == 34:
			pygame.draw.rect(win,(255,255,0),(820, a*150, 60 ,60))
			pygame.draw.rect(win,(0,0,255),(820+60, a*150, 60 ,60))

		a += 1

	#suunta = 1: oikealle
	#suunta = 2: alas
	#suunta = 3: vasemmalle
	#suunta = 4: ylös

	if suunta == 1:
		x = 870+30
		y = 590

	elif suunta == 2:
		x = 870
		y = 590+30

	elif suunta == 3:
		x = 870-30
		y = 590

	elif suunta == 4:
		x = 870
		y = 590-30

	if valittu_1 == True:
		pygame.draw.rect(win,(0,255,0),(820, 150, 120 ,60),5)

		if str(p_hand[0])[0] == "2":
			pygame.draw.rect(win,(255,0,0),(870, 590, 30 ,30))

		elif str(p_hand[0])[0] == "3":
			pygame.draw.rect(win,(255,255,0),(870, 590, 30 ,30))

		elif str(p_hand[0])[0] == "4":
			pygame.draw.rect(win,(0,0,255),(870, 590, 30 ,30))


		if str(p_hand[0])[1] == "2":
			pygame.draw.rect(win,(255,0,0),(x, y, 30 ,30))

		elif str(p_hand[0])[1] == "3":
			pygame.draw.rect(win,(255,255,0),(x, y, 30 ,30))

		elif str(p_hand[0])[1] == "4":
			pygame.draw.rect(win,(0,0,255),(x, y, 30 ,30))


	elif valittu_2 == True:
		pygame.draw.rect(win,(0,255,0),(820, 2*150, 120 ,60),5)

		if str(p_hand[1])[0] == "2":
			pygame.draw.rect(win,(255,0,0),(870, 590, 30 ,30))

		elif str(p_hand[1])[0] == "3":
			pygame.draw.rect(win,(255,255,0),(870, 590, 30 ,30))

		elif str(p_hand[1])[0] == "4":
			pygame.draw.rect(win,(0,0,255),(870, 590, 30 ,30))


		if str(p_hand[1])[1] == "2":
			pygame.draw.rect(win,(255,0,0),(x, y, 30 ,30))

		elif str(p_hand[1])[1] == "3":
			pygame.draw.rect(win,(255,255,0),(x, y, 30 ,30))

		elif str(p_hand[1])[1] == "4":
			pygame.draw.rect(win,(0,0,255),(x, y, 30 ,30))


	elif valittu_3 == True:
		pygame.draw.rect(win,(0,255,0),(820, 3*150, 120 ,60),5)

		if str(p_hand[2])[0] == "2":
			pygame.draw.rect(win,(255,0,0),(870, 590, 30 ,30))

		elif str(p_hand[2])[0] == "3":
			pygame.draw.rect(win,(255,255,0),(870, 590, 30 ,30))

		elif str(p_hand[2])[0] == "4":
			pygame.draw.rect(win,(0,0,255),(870, 590, 30 ,30))


		if str(p_hand[2])[1] == "2":
			pygame.draw.rect(win,(255,0,0),(x, y, 30 ,30))

		elif str(p_hand[2])[1] == "3":
			pygame.draw.rect(win,(255,255,0),(x, y, 30 ,30))

		elif str(p_hand[2])[1] == "4":
			pygame.draw.rect(win,(0,0,255),(x, y, 30 ,30))

	win.blit(flip_kuva,(840,680))

	#visualisoidaan alueiden omistajuus
	font2 = pygame.font.SysFont("comicsans", 15)
	ai_text = font2.render("AI", 1, (100,25,100))
	player_text = font2.render("Pelaaja", 1, (100,25,100))
	for i in range(len(omistuslauta)):
		for j in range(len(omistuslauta)):
			if omistuslauta[i][j] == 0:
				win.blit(ai_text,(j*(780/13),i*(780/13)))

			elif omistuslauta[i][j] == 1:
				win.blit(player_text,(j*(780/13),i*(780/13)))


	villagelauta = villagelauta_update(omistuslauta,lauta)

	#visualisoidaan villagen omistajuus
	ai_text_v = font2.render("AI", 1, (255,255,255))
	player_text_v = font2.render("Pelaaja", 1, (255,255,255))
	for i in range(len(villagelauta)):
		for j in range(len(villagelauta)):
			if villagelauta[i][j] == 0:
				win.blit(ai_text_v,(j*(780/13),i*(780/13)))
			elif villagelauta[i][j] == 1:
				win.blit(player_text_v,(j*(780/13),i*(780/13)))

	font = pygame.font.SysFont("comicsans", 50)
	ai_pisteet = font.render("AI: "+str(pisteet[0]), 1, (100,25,100))
	player_pisteet = font.render("Player: "+str(pisteet[1]), 1, (100,25,100))


	win.blit(player_pisteet, (800,50))
	win.blit(ai_pisteet, (800,10))


	pygame.display.update()

def omistuslauta_update(pala,y,x,y2,x2,lauta,vuoro,omistuslauta,old_lauta):
	global pisteet, printtaile

	#käydään läpi ensin tilanteet, jossa pala on tupla
	if pala==22 or pala==33 or pala==44:
		done = False
		koko, alueen_palat = scanner(y,x,lauta)

		#jos alue on kokonaan uusi tai pala lisättiin yhden palan alueeseen, annetaan omistajuus palan laittaneelle
		if koko == 2 or koko == 3:
			for palikka in alueen_palat:
				omistuslauta[palikka[0]][palikka[1]] = vuoro

			done = True

		#harvinainen tapaus, jossa tupla pala yhdistää 2 yksinäistä palaa isoksi neljän alueeksi
		if koko == 4:
			#koska omistuslautaa ei ole vielä päivitetty tässä vaiheessa, niin katsotaan jos joku uuden alueen paloista oli ennen omistamaton
			for palikka in alueen_palat:
				if omistuslauta[palikka[0]][palikka[1]] != 2:
					break
			else:
				for palikka in alueen_palat:
					omistuslauta[palikka[0]][palikka[1]] = vuoro

				done = True


		if not done:
			done_again = False

			#implementoidaan alueiden varastaminen
			omistajat = []
			for palikka in alueen_palat:
				omistajat.append([omistuslauta[palikka[0]][palikka[1]],palikka[0],palikka[1]])


			#katsotaan onko kaksi eri omistajan aluetta yhdistetty
			for omistaja in omistajat:
				for i in range(len(omistajat)):
					if omistaja[0] != 2:
						if omistajat[i][0] != 2:
							if omistaja[0] != omistajat[i][0]:
								talteen_1 = omistajat[i]
								talteen_2 = omistaja
								done_again = True
								break



			#jos löydetään, että kaksi eri omistajan aluetta on yhdistetty niin katsotaan kumman alue on suurempi
			if done_again:
				alue_1_koko, _ = scanner(talteen_1[1],talteen_1[2],old_lauta)
				alue_2_koko, _ = scanner(talteen_2[1],talteen_2[2],old_lauta)

				if alue_1_koko > alue_2_koko:
					for palikka in alueen_palat:
						omistuslauta[palikka[0]][palikka[1]] = talteen_1[0]

				elif alue_2_koko > alue_1_koko:			
					for palikka in alueen_palat:
						omistuslauta[palikka[0]][palikka[1]] = talteen_2[0]

				else:
					if vuoro == 0:
						anna = 1

					else:
						anna = 0

					for palikka in alueen_palat:
						omistuslauta[palikka[0]][palikka[1]] = anna



			#TÄSSÄ VIKA!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
			else:
				#Jos lisätään jo ennestään omistettuun alueeseen
				for palikka in alueen_palat:
					if omistuslauta[palikka[0]][palikka[1]] != 2:
						omistaja = omistuslauta[palikka[0]][palikka[1]]
						break

				for palikka in alueen_palat:
					omistuslauta[palikka[0]][palikka[1]] = omistaja

	#käydään läpi tilanteet, jossa pala ei ole tupla
	elif pala==23 or pala==24 or pala==34:
		done = False

		#tarkastellaan palaa väri kerrallaan
		koko_1, alueen_palat_1 = scanner(y,x,lauta)



		#harvinainen tapaus, jossa single pala yhdistää 2 yksinäistä palaa kolmen alueeksi
		if koko_1 == 3:
			for palikka in alueen_palat_1:
				if omistuslauta[palikka[0]][palikka[1]] != 2:
					break
			else:
				for palikka in alueen_palat_1:
					omistuslauta[palikka[0]][palikka[1]] = vuoro

				done = True


		if not done:
				done_again = False
				#implementoidaan alueiden varastaminen
				omistajat = []
				for palikka in alueen_palat_1:
					omistajat.append([omistuslauta[palikka[0]][palikka[1]],palikka[0],palikka[1]])


				#katsotaan onko kaksi eri omistajan aluetta yhdistetty
				for omistaja in omistajat:
					for i in range(len(omistajat)):
						if omistaja[0] != 2:
							if omistajat[i][0] != 2:
								if omistaja[0] != omistajat[i][0]:
									talteen_1 = omistajat[i]
									talteen_2 = omistaja
									done_again = True
									break

				#jos löydetään, että kaksi eri omistajan aluetta on yhdistetty niin katsotaan kumman alue on suurempi
				if done_again:
					alue_1_koko, _ = scanner(talteen_1[1],talteen_1[2],old_lauta)
					alue_2_koko, _ = scanner(talteen_2[1],talteen_2[2],old_lauta)

					if alue_1_koko > alue_2_koko:
						for palikka in alueen_palat_1:
							omistuslauta[palikka[0]][palikka[1]] = talteen_1[0]

					elif alue_2_koko > alue_1_koko:			
						for palikka in alueen_palat_1:
							omistuslauta[palikka[0]][palikka[1]] = talteen_2[0]

					else:
						if vuoro == 0:
							anna = 1

						else:
							anna = 0

						for palikka in alueen_palat_1:
							omistuslauta[palikka[0]][palikka[1]] = anna


				else:
					#jos lisättiin jo omistettuun alueeseen
					if koko_1 > 2:
						for palikka in alueen_palat_1:
							if omistuslauta[palikka[0]][palikka[1]] != 2:
								omistaja = omistuslauta[palikka[0]][palikka[1]]
								break

						for palikka in alueen_palat_1:
							done_again = True
							omistuslauta[palikka[0]][palikka[1]] = omistaja



		#tarkastellaan nyt palan toista väriä
		koko_2, alueen_palat_2 = scanner(y2,x2,lauta)

		#harvinainen tapaus, jossa single pala yhdistää 2 yksinäistä palaa kolmen alueeksi
		done = False
		if koko_2 == 3:
			for palikka in alueen_palat_2:
				if omistuslauta[palikka[0]][palikka[1]] != 2:
					break
			else:
				for palikka in alueen_palat_2:
					omistuslauta[palikka[0]][palikka[1]] = vuoro

				done = True

		if not done:
			done_again = False
			#implementoidaan alueiden varastaminen
			omistajat = []
			for palikka in alueen_palat_2:
				omistajat.append([omistuslauta[palikka[0]][palikka[1]],palikka[0],palikka[1]])


			#katsotaan onko kaksi eri omistajan aluetta yhdistetty
			for omistaja in omistajat:
				for i in range(len(omistajat)):
					if omistaja[0] != 2:
						if omistajat[i][0] != 2:
							if omistaja[0] != omistajat[i][0]:
								talteen_1 = omistajat[i]
								talteen_2 = omistaja
								done_again = True
								break

			#jos löydetään, että kaksi eri omistajan aluetta on yhdistetty niin katsotaan kumman alue on suurempi
			if done_again:
				alue_1_koko, _ = scanner(talteen_1[1],talteen_1[2],old_lauta)
				alue_2_koko, _ = scanner(talteen_2[1],talteen_2[2],old_lauta)

				if alue_1_koko > alue_2_koko:
					for palikka in alueen_palat_2:
						omistuslauta[palikka[0]][palikka[1]] = talteen_1[0]

				elif alue_2_koko > alue_1_koko:			
					for palikka in alueen_palat_2:
						omistuslauta[palikka[0]][palikka[1]] = talteen_2[0]

				else:
					if vuoro == 0:
						anna = 1

					else:
						anna = 0

					for palikka in alueen_palat_2:
						omistuslauta[palikka[0]][palikka[1]] = anna

			else:
				#jos lisättiin jo omistettuun alueeseen
				if koko_2 > 2:
					for palikka in alueen_palat_2:
						if omistuslauta[palikka[0]][palikka[1]] != 2:
							omistaja = omistuslauta[palikka[0]][palikka[1]]
							break

					for palikka in alueen_palat_2:
						done_again = True
						omistuslauta[palikka[0]][palikka[1]] = omistaja


		#sitten tarkastellaan tilannetta, jossa palan lisääminen luo uuden alueen
		if koko_1 == 2:
			for palikka in alueen_palat_1:
				omistuslauta[palikka[0]][palikka[1]] = vuoro

		if koko_2 == 2:
			for palikka in alueen_palat_2:
				omistuslauta[palikka[0]][palikka[1]] = vuoro

	return omistuslauta

def xy2(suunta,y,x):
	if suunta == 1:
		x_2 = x+1 
		y_2 = y

	elif suunta == 2:
		x_2 = x 
		y_2 = y+1

	elif suunta == 3:
		x_2 = x-1 
		y_2 = y

	elif suunta == 4:
		x_2 = x 
		y_2 = y-1

	return y_2,x_2

def hover(pala,suunta,mouse):
	global renderöi

	renderöi = False

	win.fill((200,200,200))
	#mouse = pygame.mouse.get_pos()
	hover_x = int(mouse[0]/60)
	hover_y = int(mouse[1]/60)

	y2,x2 = xy2(suunta,hover_y,hover_x)

	if mouse[0]<780:
		if suunta == 1:
			if mouse[0]<720:
				if int(str(pala)[0]) == 2:
					pygame.draw.rect(win,(255,0,0),(hover_x*60, hover_y*60, 60, 60))

				elif int(str(pala)[0]) == 3:
					pygame.draw.rect(win,(255,255,0),(hover_x*60, hover_y*60, 60, 60))

				elif int(str(pala)[0]) == 4:
					pygame.draw.rect(win,(0,0,255),(hover_x*60, hover_y*60, 60, 60))


				if int(str(pala)[1]) == 2:
					pygame.draw.rect(win,(255,0,0),(x2*60, y2*60, 60, 60))

				elif int(str(pala)[1]) == 3:
					pygame.draw.rect(win,(255,255,0),(x2*60, y2*60, 60, 60))

				elif int(str(pala)[1]) == 4:
					pygame.draw.rect(win,(0,0,255),(x2*60, y2*60, 60, 60))

		else:
			if int(str(pala)[0]) == 2:
				pygame.draw.rect(win,(255,0,0),(hover_x*60, hover_y*60, 60, 60))

			elif int(str(pala)[0]) == 3:
				pygame.draw.rect(win,(255,255,0),(hover_x*60, hover_y*60, 60, 60))

			elif int(str(pala)[0]) == 4:
				pygame.draw.rect(win,(0,0,255),(hover_x*60, hover_y*60, 60, 60))


			if int(str(pala)[1]) == 2:
				pygame.draw.rect(win,(255,0,0),(x2*60, y2*60, 60, 60))

			elif int(str(pala)[1]) == 3:
				pygame.draw.rect(win,(255,255,0),(x2*60, y2*60, 60, 60))

			elif int(str(pala)[1]) == 4:
				pygame.draw.rect(win,(0,0,255),(x2*60, y2*60, 60, 60))


	display(omistuslauta,lauta)

	pygame.display.update()



def siirto(old_lauta):
	global valittu_1,valittu_2,valittu_3,suunta,palanen,p_hand,pakka,vuoro,new,omistuslauta,pisteet,first

	pygame.event.get()
	mouse = pygame.mouse.get_pos()
	click = pygame.mouse.get_pressed()

	#if first:
	#	win.fill((200,200,200))
	#	display(omistuslauta,lauta)
	#	first = False

	#kortin valinta
	if 820<mouse[0]<(820+120):
		if click[0] == 1:
			#klikataan ylintä korttia
			if 150<mouse[1]<(150+60):
				time.sleep(0.2)
				valittu_1 = True
				valittu_2 = False
				valittu_3 = False
				suunta = 1
				palanen = p_hand[0]

			elif 2*150<mouse[1]<(2*150+60):
				time.sleep(0.2)
				valittu_2 = True
				valittu_1 = False
				valittu_3 = False
				suunta = 1
				palanen = p_hand[1]


			elif 3*150<mouse[1]<(3*150+60):
				time.sleep(0.2)
				valittu_3 = True
				valittu_1 = False
				valittu_2 = False
				suunta = 1
				palanen = p_hand[2]

	#kortin kääntely
	if 840<mouse[0]<(840+80) and 680<mouse[1]<680+80 and click[0] == 1:
		time.sleep(0.2)
		suunta += 1
		if suunta == 5:
			suunta = 1

	if palanen != None:
		hover(palanen,suunta,mouse)

	#kortin laittaminen laudalle
	if click[0] == 1 and 0<mouse[0]<780 and 0<mouse[1]<780:
		time.sleep(0.2)
		lauta_x = int(mouse[0]/60)
		lauta_y = int(mouse[1]/60)

		#suunta määrää, mihin toinen osa palasta menee
		if suunta == 1:
			lauta_x_2 = lauta_x+1 
			lauta_y_2 = lauta_y

		elif suunta == 2:
			lauta_x_2 = lauta_x 
			lauta_y_2 = lauta_y+1

		elif suunta == 3:
			lauta_x_2 = lauta_x-1 
			lauta_y_2 = lauta_y

		elif suunta == 4:
			lauta_x_2 = lauta_x 
			lauta_y_2 = lauta_y-1

		#jos pelaajan yrittämä siirto on laillinen
		if palanen != None and [lauta_y,lauta_x,suunta,palanen] in legal_moves(palanen,lauta):

			#laitetaan pala laudalle
			lauta[lauta_y][lauta_x] = int(str(palanen)[0])
			lauta[lauta_y_2][lauta_x_2] = int(str(palanen)[1])


			#päivitetään omistuslauta
			omistuslauta = omistuslauta_update(palanen,lauta_y,lauta_x,lauta_y_2,lauta_x_2,lauta,vuoro,omistuslauta,old_lauta)


			#print("")
			#for k in range(13):
			#	print(omistuslauta[k])


			#päivitetään kädessä olevat palat
			p_hand.remove(palanen)
			uusi_pala = random.choice(pakka)
			p_hand.append(uusi_pala)
			pakka.remove(uusi_pala)

			#resetataan valinnat
			valittu_1 = False
			valittu_2 = False
			valittu_3 = False

			palanen = None

			#päivitetään pisteet
			pisteet = evaluation(lauta,omistuslauta)

			#real_pisteet[0] = pisteet[0]+villagepisteet_ai
			#real_pisteet[1] = pisteet[1]+villagepisteet_pelaaja

			if vuoro == 0:
				vuoro = 1

			else:
				vuoro = 0

			new = True
			renderöi = True

		else:
			pass

	return omistuslauta

def legal_moves(pala,lauta):
	#moves = [[y,x,suunta]]
	moves = []

	pala_1 = int(str(pala)[0])
	pala_2 = int(str(pala)[1])

	for i in range(len(lauta)):
		for j in range(len(lauta)):

			#SUUNTA = 1
			#laudalla olevasta laatasta voi lisätä oikealle jos on tyhjää
			if j+2<=len(lauta)-1 and lauta[i][j]!=0 and lauta[i][j]!=1 and lauta[i][j+1]==0 and lauta[i][j+2]==0:
				moves.append([i,j+1,1,pala])

			#laudalla olevasta laatasta voi lisätä vasemmalle jos on tyhjää
			if j-2>=0 and lauta[i][j]!=0 and lauta[i][j]!=1 and lauta[i][j-1]==0 and lauta[i][j-2]==0:
				moves.append([i,j-2,1,pala])

			#laudalla olevan laatan päälle oikealle lisääminen
			if i-1>=0 and j+1<=len(lauta)-1 and lauta[i][j]!=0 and lauta[i][j]!=1 and lauta[i-1][j]==0 and lauta[i-1][j+1]==0:
				moves.append([i-1,j,1,pala])

			#laudalla olevan laatan päälle vasemmalle lisääminen
			if i-1>=0 and j-1>=0 and lauta[i][j]!=0 and lauta[i][j]!=1 and lauta[i-1][j]==0 and lauta[i-1][j-1]==0:
				moves.append([i-1,j-1,1,pala])

			#laudalla olevan laatan alle oikealle lisääminen
			if i+1<=len(lauta)-1 and j+1<=len(lauta)-1 and lauta[i][j]!=0 and lauta[i][j]!=1 and lauta[i+1][j]==0 and lauta[i+1][j+1]==0:
				moves.append([i+1,j,1,pala])

			#laudalla olevan laatan alle vasemmalle lisääminen
			if i+1<=len(lauta)-1 and j-1>=0 and lauta[i][j]!=0 and lauta[i][j]!=1 and lauta[i+1][j]==0 and lauta[i+1][j-1]==0:
				moves.append([i+1,j-1,1,pala])




			#SUUNTA = 2
			#oikealle alas
			if j+1<=len(lauta)-1 and i+1<=len(lauta)-1 and lauta[i][j]!=0 and lauta[i][j]!=1 and lauta[i][j+1]==0 and lauta[i+1][j+1]==0:
				moves.append([i,j+1,2,pala])

			#oikealle ylös
			if j+1<=len(lauta)-1 and i-1>=0 and lauta[i][j]!=0 and lauta[i][j]!=1 and lauta[i][j+1]==0 and lauta[i-1][j+1]==0:
				moves.append([i-1,j+1,2,pala])

			#vasemmalle alas
			if j-1>=0 and i+1<=len(lauta)-1 and lauta[i][j]!=0 and lauta[i][j]!=1 and lauta[i][j-1]==0 and lauta[i+1][j-1]==0:
				moves.append([i,j-1,2,pala])

			#vasemmalle ylös
			if j-1>=0 and i-1>=0 and lauta[i][j]!=0 and lauta[i][j]!=1 and lauta[i][j-1]==0 and lauta[i-1][j-1]==0:
				moves.append([i-1,j-1,2,pala])

			#yläpuolelle
			if i-2>=0 and lauta[i][j]!=0 and lauta[i][j]!=1 and lauta[i-1][j]==0 and lauta[i-2][j]==0:
				moves.append([i-2,j,2,pala])

			#alapuolelle
			if i+2<=len(lauta)-1 and lauta[i][j]!=0 and lauta[i][j]!=1 and lauta[i+1][j]==0 and lauta[i+2][j]==0:
				moves.append([i+1,j,2,pala])




			#SUUNTA = 3
			#oikealle
			if j+2<=len(lauta)-1 and lauta[i][j]!=0 and lauta[i][j]!=1 and lauta[i][j+1]==0 and lauta[i][j+2]==0:
				moves.append([i,j+2,3,pala])

			#laudalla olevasta laatasta voi lisätä vasemmalle jos on tyhjää
			if j-2>=0 and lauta[i][j]!=0 and lauta[i][j]!=1 and lauta[i][j-1]==0 and lauta[i][j-2]==0:
				moves.append([i,j-1,3,pala])

			#laudalla olevan laatan päälle oikealle lisääminen
			if i-1>=0 and j+1<=len(lauta)-1 and lauta[i][j]!=0 and lauta[i][j]!=1 and lauta[i-1][j]==0 and lauta[i-1][j+1]==0:
				moves.append([i-1,j+1,3,pala])

			#laudalla olevan laatan päälle vasemmalle lisääminen
			if i-1>=0 and j-1>=0 and lauta[i][j]!=0 and lauta[i][j]!=1 and lauta[i-1][j]==0 and lauta[i-1][j-1]==0:
				moves.append([i-1,j,3,pala])

			#laudalla olevan laatan alle oikealle lisääminen
			if i+1<=len(lauta)-1 and j+1<=len(lauta)-1 and lauta[i][j]!=0 and lauta[i][j]!=1 and lauta[i+1][j]==0 and lauta[i+1][j+1]==0:
				moves.append([i+1,j+1,3,pala])

			#laudalla olevan laatan alle vasemmalle lisääminen
			if i+1<=len(lauta)-1 and j-1>=0 and lauta[i][j]!=0 and lauta[i][j]!=1 and lauta[i+1][j]==0 and lauta[i+1][j-1]==0:
				moves.append([i+1,j,3,pala])




			#SUUNTA = 4
			#oikealle alas
			if j+1<=len(lauta)-1 and i+1<=len(lauta)-1 and lauta[i][j]!=0 and lauta[i][j]!=1 and lauta[i][j+1]==0 and lauta[i+1][j+1]==0:
				moves.append([i+1,j+1,4,pala])

			#oikealle ylös
			if j+1<=len(lauta)-1 and i-1>=0 and lauta[i][j]!=0 and lauta[i][j]!=1 and lauta[i][j+1]==0 and lauta[i-1][j+1]==0:
				moves.append([i,j+1,4,pala])

			#vasemmalle alas
			if j-1>=0 and i+1<=len(lauta)-1 and lauta[i][j]!=0 and lauta[i][j]!=1 and lauta[i][j-1]==0 and lauta[i+1][j-1]==0:
				moves.append([i+1,j-1,4,pala])

			#vasemmalle ylös
			if j-1>=0 and i-1>=0 and lauta[i][j]!=0 and lauta[i][j]!=1 and lauta[i][j-1]==0 and lauta[i-1][j-1]==0:
				moves.append([i,j-1,4,pala])

			#yläpuolelle
			if i-2>=0 and lauta[i][j]!=0 and lauta[i][j]!=1 and lauta[i-1][j]==0 and lauta[i-2][j]==0:
				moves.append([i-1,j,4,pala])

			#alapuolelle
			if i+2<=len(lauta)-1 and lauta[i][j]!=0 and lauta[i][j]!=1 and lauta[i+1][j]==0 and lauta[i+2][j]==0:
				moves.append([i+2,j,4,pala])

	return moves


def scanner_help(y,x,board,samat_palat,koko):

	#skannataan vasemmalle
	if x-1>=0 and board[y][x-1] == board[y][x] and [y,x-1] not in samat_palat:
		koko += 1
		samat_palat.append([y,x-1])

	#oikealle
	if x+1<=12 and board[y][x+1] == board[y][x] and [y,x+1] not in samat_palat:
		koko += 1
		samat_palat.append([y,x+1])

	#ylös
	if y-1>=0 and board[y-1][x] == board[y][x] and [y-1,x] not in samat_palat:
		koko += 1
		samat_palat.append([y-1,x])

	#alas
	if y+1<=12 and board[y+1][x] == board[y][x] and [y+1,x] not in samat_palat:
		koko += 1
		samat_palat.append([y+1,x])

	return samat_palat, koko

#laskee moneen samanväriseen palaan sille annettu pala on yhdistettynä
def scanner(y,x,board):
	koko = 1
	samat_palat = [[y,x]]

	#Miten toimii?
	#skannataan annetusta palasta 1 ruutu jokaiseen suuntaan, jonka jälkeen lisätään skannatut saman väriset palat listaan, jottei niitä lisätä kokoon uudestaan
	#sen jälkeen valitaan yksi kerrallaan skannatuista paloista paljastunut saman värinen pala ja tehdään ylempi vaihe sille ja tämä tehdään kunnes ei löydetä enää uusia paloja

	i = 0
	while True:
		try:
			samat_palat,koko = scanner_help(samat_palat[i][0],samat_palat[i][1],board,samat_palat,koko)
			i += 1
		except:
			break

	return koko,samat_palat


def villagelauta_update(omistuslauta,lauta):
	global villagelauta
	#luodaan villagelauta aina uudestaan, koska joka ikinen village käydään kuitenkin läpi
	#villagelaudassa 0 tarkoittaa, että AI omistaa villagen ja 1, että pelaaja omistaa villagen ja 2, että villagea ei omisteta/ei ole villagea

	#villagelauta = []
	#for i in range(13):
	#	villagelauta.append([2,2,2,2,2,2,2,2,2,2,2,2,2])


	villagespots = [[0,0],[0,12],[2,9],[4,0],[8,1],[9,9],[12,12]]

	tuplavillaget = [[2,4],[5,12],[10,5],[12,0]]


	for i in range(len(villagespots)):
		vasen = False
		oikea = False
		ylä = False

		kontrollointipisteet_ai = 0
		kontrollointipisteet_pelaaja = 0

		kylä = [villagespots[i][0],villagespots[i][1]]

		#ensin käydään kylän vasenta reunaa koskeva alue
		if kylä[1]-1 >= 0:
			vasen_omistaja = omistuslauta[kylä[0]][kylä[1]-1]
			#jos alueella on omistaja
			if vasen_omistaja != 2:
				vasen = True
				#katsotaan alueen koko ja palat
				koko_vasen, palat_vasen = scanner(kylä[0], kylä[1]-1, lauta)

				#jos koko on alle 5, annetaan 1 kontrollointipiste
				if koko_vasen <5:
					if vasen_omistaja == 0:
						kontrollointipisteet_ai += 1
					else:
						kontrollointipisteet_pelaaja += 1
				#ja jos koko on yli 5 annetaan 2 kontrollointipistettä
				else:
					if vasen_omistaja == 0:
						kontrollointipisteet_ai += 2
					else:
						kontrollointipisteet_pelaaja += 2


		#sitten kylän yläreuna
		if kylä[0]-1 >= 0:
			ylä_omistaja = omistuslauta[kylä[0]-1][kylä[1]]

			if ylä_omistaja != 2:
				ylä = True
				koko_ylä, palat_ylä = scanner(kylä[0]-1, kylä[1], lauta)

				#tarkistetaan koskettaako yksi alue ylä ja vasenta sivua
				sama_alue = False
				for pala in palat_ylä:

					#vältytään erroreilta, koska jos vasemmalla sivulla ei ole palaa ollenkaan, niin pala_vasen ei ole olemassa
					if vasen:
						if pala in palat_vasen:
							sama_alue = True
							break

				#jos ei...
				if sama_alue == False:
					#jos koko on alle 5, annetaan 1 kontrollointipiste
					if koko_ylä <5:
						if ylä_omistaja == 0:
							kontrollointipisteet_ai += 1
						else:
							kontrollointipisteet_pelaaja += 1
					#ja jos koko on yli 5 annetaan 2 kontrollointipistettä
					else:
						if ylä_omistaja == 0:
							kontrollointipisteet_ai += 2
						else:
							kontrollointipisteet_pelaaja += 2



		#sitten kylän oikea reuna
		if kylä[1]+1 <= 12:
			oikea_omistaja = omistuslauta[kylä[0]][kylä[1]+1]

			if oikea_omistaja != 2:
				oikea = True
				koko_oikea, palat_oikea = scanner(kylä[0], kylä[1]+1, lauta)


				#tarkistetaan koskettaako yksi alue montaa kylän sivua
				sama_alue = False
				for pala in palat_oikea:
					if vasen:
						if pala in palat_vasen:
							sama_alue = True
							break
					if ylä:
						if pala in palat_ylä:
							sama_alue = True
							break


				#jos ei...
				if sama_alue == False:
					#jos koko on alle 5, annetaan 1 kontrollointipiste
					if koko_oikea <5:
						if oikea_omistaja == 0:
							kontrollointipisteet_ai += 1
						else:
							kontrollointipisteet_pelaaja += 1
					#ja jos koko on yli 5 annetaan 2 kontrollointipistettä
					else:
						if oikea_omistaja == 0:
							kontrollointipisteet_ai += 2
						else:
							kontrollointipisteet_pelaaja += 2




		#sitten kylän alareuna
		if kylä[0]+1 <= 12:
			ala_omistaja = omistuslauta[kylä[0]+1][kylä[1]]

			if ala_omistaja != 2:
				koko_ala, palat_ala = scanner(kylä[0]+1, kylä[1], lauta)

				#tarkistetaan koskettaako yksi alue montaa kylän sivua
				sama_alue = False
				for pala in palat_ala:
					if vasen:
						if pala in palat_vasen:
							sama_alue = True
							break

					if ylä:
						if pala in palat_ylä:
							sama_alue = True
							break

					if oikea:
						if pala in palat_oikea:
							sama_alue = True
							break

				#jos ei...
				if sama_alue == False:
					#jos koko on alle 5, annetaan 1 kontrollointipiste
					if koko_ala <5:
						if ala_omistaja == 0:
							kontrollointipisteet_ai += 1
						else:
							kontrollointipisteet_pelaaja += 1
					#ja jos koko on yli 5 annetaan 2 kontrollointipistettä
					else:
						if ala_omistaja == 0:
							kontrollointipisteet_ai += 2
						else:
							kontrollointipisteet_pelaaja += 2

		#if kylä == [4,0]:
		#	print("PELAAJA:",kontrollointipisteet_pelaaja)
		#	print("AI:",kontrollointipisteet_ai)
		#	print("------------------------------------")

		if kontrollointipisteet_pelaaja == 0 and kontrollointipisteet_ai == 0:
			villagelauta[villagespots[i][0]][villagespots[i][1]] = 2

		elif kontrollointipisteet_pelaaja > kontrollointipisteet_ai:
			villagelauta[villagespots[i][0]][villagespots[i][1]] = 1

		elif kontrollointipisteet_ai > kontrollointipisteet_pelaaja:
			villagelauta[villagespots[i][0]][villagespots[i][1]] = 0


	for i in range(len(tuplavillaget)):

		#vaakatuplavillaget
		if tuplavillaget[i] == [2,4] or tuplavillaget[i] == [12,0]:
			vasen = False
			oikea = False
			ylä_vasen = False
			ylä_oikea = False
			ala_vasen = False

			kontrollointipisteet_ai = 0
			kontrollointipisteet_pelaaja = 0

			kylä = [tuplavillaget[i][0],tuplavillaget[i][1]]

			#ensin käydään kylän vasenta reunaa koskeva alue
			if kylä[1]-1 >= 0:
				vasen_omistaja = omistuslauta[kylä[0]][kylä[1]-1]
				#jos alueella on omistaja
				if vasen_omistaja != 2:
					vasen = True
					#katsotaan alueen koko ja palat
					koko_vasen, palat_vasen = scanner(kylä[0], kylä[1]-1, lauta)

					#jos koko on alle 5, annetaan 1 kontrollointipiste
					if koko_vasen <5:
						if vasen_omistaja == 0:
							kontrollointipisteet_ai += 1
						else:
							kontrollointipisteet_pelaaja += 1
					#ja jos koko on yli 5 annetaan 2 kontrollointipistettä
					else:
						if vasen_omistaja == 0:
							kontrollointipisteet_ai += 2
						else:
							kontrollointipisteet_pelaaja += 2


			#sitten kylän vasen yläreuna
			if kylä[0]-1 >= 0:
				ylä_omistaja = omistuslauta[kylä[0]-1][kylä[1]]

				if ylä_omistaja != 2:
					ylä_vasen = True
					koko_ylä, palat_ylä_vasen = scanner(kylä[0]-1, kylä[1], lauta)

					#tarkistetaan koskettaako yksi alue ylä ja vasenta sivua
					sama_alue = False
					for pala in palat_ylä_vasen:

						#vältytään erroreilta, koska jos vasemmalla sivulla ei ole palaa ollenkaan, niin pala_vasen ei ole olemassa
						if vasen:
							if pala in palat_vasen:
								sama_alue = True
								break

					#jos ei...
					if sama_alue == False:
						#jos koko on alle 5, annetaan 1 kontrollointipiste
						if koko_ylä <5:
							if ylä_omistaja == 0:
								kontrollointipisteet_ai += 1
							else:
								kontrollointipisteet_pelaaja += 1
						#ja jos koko on yli 5 annetaan 2 kontrollointipistettä
						else:
							if ylä_omistaja == 0:
								kontrollointipisteet_ai += 2
							else:
								kontrollointipisteet_pelaaja += 2


			#sitten kylä oikea yläreuna
			if kylä[0]-1 >= 0:
				ylä_omistaja = omistuslauta[kylä[0]-1][kylä[1]+1]

				if ylä_omistaja != 2:
					ylä_oikea = True
					koko_ylä, palat_ylä_oikea = scanner(kylä[0]-1, kylä[1]+1, lauta)

					#tarkistetaan koskettaako yksi alue ylä ja vasenta sivua
					sama_alue = False
					for pala in palat_ylä_oikea:

						#vältytään erroreilta, koska jos vasemmalla sivulla ei ole palaa ollenkaan, niin pala_vasen ei ole olemassa
						if vasen:
							if pala in palat_vasen:
								sama_alue = True
								break

						if ylä_vasen:
							if pala in palat_ylä_vasen:
								sama_alue = True
								break

					#jos ei...
					if sama_alue == False:
						#jos koko on alle 5, annetaan 1 kontrollointipiste
						if koko_ylä <5:
							if ylä_omistaja == 0:
								kontrollointipisteet_ai += 1
							else:
								kontrollointipisteet_pelaaja += 1
						#ja jos koko on yli 5 annetaan 2 kontrollointipistettä
						else:
							if ylä_omistaja == 0:
								kontrollointipisteet_ai += 2
							else:
								kontrollointipisteet_pelaaja += 2


			#sitten kylän oikea reuna
			if kylä[1]+2 <= 12:
				oikea_omistaja = omistuslauta[kylä[0]][kylä[1]+2]

				if oikea_omistaja != 2:
					oikea = True
					koko_oikea, palat_oikea = scanner(kylä[0], kylä[1]+2, lauta)


					#tarkistetaan koskettaako yksi alue montaa kylän sivua
					sama_alue = False
					for pala in palat_oikea:
						if vasen:
							if pala in palat_vasen:
								sama_alue = True
								break
						if ylä_vasen:
							if pala in palat_ylä_vasen:
								sama_alue = True
								break
						if ylä_oikea:
							if pala in palat_ylä_oikea:
								sama_alue = True
								break


					#jos ei...
					if sama_alue == False:
						#jos koko on alle 5, annetaan 1 kontrollointipiste
						if koko_oikea <5:
							if oikea_omistaja == 0:
								kontrollointipisteet_ai += 1
							else:
								kontrollointipisteet_pelaaja += 1
						#ja jos koko on yli 5 annetaan 2 kontrollointipistettä
						else:
							if oikea_omistaja == 0:
								kontrollointipisteet_ai += 2
							else:
								kontrollointipisteet_pelaaja += 2


			#sitten kylän vasen alareuna
			if kylä[0]+1 <= 12:
				ala_omistaja = omistuslauta[kylä[0]+1][kylä[1]]

				if ala_omistaja != 2:
					ala_vasen = True
					koko_ala, palat_ala_vasen = scanner(kylä[0]+1, kylä[1], lauta)

					#tarkistetaan koskettaako yksi alue montaa kylän sivua
					sama_alue = False
					for pala in palat_ala_vasen:
						if vasen:
							if pala in palat_vasen:
								sama_alue = True
								break

						if ylä_vasen:
							if pala in palat_ylä_vasen:
								sama_alue = True
								break

						if ylä_oikea:
							if pala in palat_ylä_oikea:
								sama_alue = True
								break

						if oikea:
							if pala in palat_oikea:
								sama_alue = True
								break

					#jos ei...
					if sama_alue == False:
						#jos koko on alle 5, annetaan 1 kontrollointipiste
						if koko_ala <5:
							if ala_omistaja == 0:
								kontrollointipisteet_ai += 1
							else:
								kontrollointipisteet_pelaaja += 1
						#ja jos koko on yli 5 annetaan 2 kontrollointipistettä
						else:
							if ala_omistaja == 0:
								kontrollointipisteet_ai += 2
							else:
								kontrollointipisteet_pelaaja += 2

			#sitten kylän oikea alareuna
			if kylä[0]+1 <= 12:
				ala_omistaja = omistuslauta[kylä[0]+1][kylä[1]+1]

				if ala_omistaja != 2:
					koko_ala, palat_ala_oikea = scanner(kylä[0]+1, kylä[1]+1, lauta)

					#tarkistetaan koskettaako yksi alue montaa kylän sivua
					sama_alue = False
					for pala in palat_ala_oikea:
						if vasen:
							if pala in palat_vasen:
								sama_alue = True
								break

						if ylä_vasen:
							if pala in palat_ylä_vasen:
								sama_alue = True
								break

						if ylä_oikea:
							if pala in palat_ylä_oikea:
								sama_alue = True
								break

						if oikea:
							if pala in palat_oikea:
								sama_alue = True
								break

						if ala_vasen:
							if pala in palat_ala_vasen:
								sama_alue = True
								break

					#jos ei...
					if sama_alue == False:
						#jos koko on alle 5, annetaan 1 kontrollointipiste
						if koko_ala <5:
							if ala_omistaja == 0:
								kontrollointipisteet_ai += 1
							else:
								kontrollointipisteet_pelaaja += 1
						#ja jos koko on yli 5 annetaan 2 kontrollointipistettä
						else:
							if ala_omistaja == 0:
								kontrollointipisteet_ai += 2
							else:
								kontrollointipisteet_pelaaja += 2


			if kontrollointipisteet_pelaaja == 0 and kontrollointipisteet_ai == 0:
				villagelauta[tuplavillaget[i][0]][tuplavillaget[i][1]] = 2

			elif kontrollointipisteet_pelaaja > kontrollointipisteet_ai:
				villagelauta[tuplavillaget[i][0]][tuplavillaget[i][1]] = 1

			elif kontrollointipisteet_ai > kontrollointipisteet_pelaaja:
				villagelauta[tuplavillaget[i][0]][tuplavillaget[i][1]] = 0


		#pystytuplavillaget
		if tuplavillaget[i] == [5,12] or tuplavillaget[i] == [10,5]:
			ylä_vasen = False
			ylä_oikea = False
			ala_vasen = False
			ala_oikea = False
			ylä = False

			kontrollointipisteet_ai = 0
			kontrollointipisteet_pelaaja = 0

			kylä = [tuplavillaget[i][0],tuplavillaget[i][1]]

			#ensin käydään läpi kylän ylävasenta reunaa koskeva alue
			if kylä[1]-1 >= 0:
				vasen_omistaja = omistuslauta[kylä[0]][kylä[1]-1]
				#jos alueella on omistaja
				if vasen_omistaja != 2:
					ylä_vasen = True
					#katsotaan alueen koko ja palat
					koko_vasen, palat_vasen_ylä = scanner(kylä[0], kylä[1]-1, lauta)

					#jos koko on alle 5, annetaan 1 kontrollointipiste
					if koko_vasen <5:
						if vasen_omistaja == 0:
							kontrollointipisteet_ai += 1
						else:
							kontrollointipisteet_pelaaja += 1
					#ja jos koko on yli 5 annetaan 2 kontrollointipistettä
					else:
						if vasen_omistaja == 0:
							kontrollointipisteet_ai += 2
						else:
							kontrollointipisteet_pelaaja += 2


			#sitten kylän alavasen reuna
			if kylä[1]-1 >= 0:
				ylä_omistaja = omistuslauta[kylä[0]+1][kylä[1]-1]

				if ylä_omistaja != 2:
					ala_vasen = True
					koko_ylä, palat_vasen_ala = scanner(kylä[0]+1, kylä[1]-1, lauta)

					#tarkistetaan koskettaako yksi alue ylä ja vasenta sivua
					sama_alue = False
					for pala in palat_vasen_ala:

						#vältytään erroreilta, koska jos vasemmalla sivulla ei ole palaa ollenkaan, niin pala_vasen ei ole olemassa
						if ylä_vasen:
							if pala in palat_vasen_ylä:
								sama_alue = True
								break

					#jos ei...
					if sama_alue == False:
						#jos koko on alle 5, annetaan 1 kontrollointipiste
						if koko_ylä <5:
							if ylä_omistaja == 0:
								kontrollointipisteet_ai += 1
							else:
								kontrollointipisteet_pelaaja += 1
						#ja jos koko on yli 5 annetaan 2 kontrollointipistettä
						else:
							if ylä_omistaja == 0:
								kontrollointipisteet_ai += 2
							else:
								kontrollointipisteet_pelaaja += 2


			#sitten kylän yläoikea reuna
			if kylä[1]+1 <= 12:
				ylä_omistaja = omistuslauta[kylä[0]][kylä[1]+1]

				if ylä_omistaja != 2:
					ylä_oikea = True
					koko_ylä, palat_oikea_ylä = scanner(kylä[0], kylä[1]+1, lauta)

					#tarkistetaan koskettaako yksi alue ylä ja vasenta sivua
					sama_alue = False
					for pala in palat_oikea_ylä:

						#vältytään erroreilta, koska jos vasemmalla sivulla ei ole palaa ollenkaan, niin pala_vasen ei ole olemassa
						if ylä_vasen:
							if pala in palat_vasen_ylä:
								sama_alue = True
								break

						if ala_vasen:
							if pala in palat_vasen_ala:
								sama_alue = True
								break

					#jos ei...
					if sama_alue == False:
						#jos koko on alle 5, annetaan 1 kontrollointipiste
						if koko_ylä <5:
							if ylä_omistaja == 0:
								kontrollointipisteet_ai += 1
							else:
								kontrollointipisteet_pelaaja += 1
						#ja jos koko on yli 5 annetaan 2 kontrollointipistettä
						else:
							if ylä_omistaja == 0:
								kontrollointipisteet_ai += 2
							else:
								kontrollointipisteet_pelaaja += 2


			#sitten kylän alaoikea reuna
			if kylä[1]+1 <= 12:
				ylä_omistaja = omistuslauta[kylä[0]+1][kylä[1]+1]

				if ylä_omistaja != 2:
					ala_oikea = True
					koko_ylä, palat_oikea_ala = scanner(kylä[0]+1, kylä[1]+1, lauta)

					#tarkistetaan koskettaako yksi alue ylä ja vasenta sivua
					sama_alue = False
					for pala in palat_oikea_ala:

						#vältytään erroreilta, koska jos vasemmalla sivulla ei ole palaa ollenkaan, niin pala_vasen ei ole olemassa
						if ylä_vasen:
							if pala in palat_vasen_ylä:
								sama_alue = True
								break

						if ala_vasen:
							if pala in palat_vasen_ala:
								sama_alue = True
								break

						if ylä_oikea:
							if pala in palat_oikea_ylä:
								sama_alue = True
								break

					#jos ei...
					if sama_alue == False:
						#jos koko on alle 5, annetaan 1 kontrollointipiste
						if koko_ylä <5:
							if ylä_omistaja == 0:
								kontrollointipisteet_ai += 1
							else:
								kontrollointipisteet_pelaaja += 1
						#ja jos koko on yli 5 annetaan 2 kontrollointipistettä
						else:
							if ylä_omistaja == 0:
								kontrollointipisteet_ai += 2
							else:
								kontrollointipisteet_pelaaja += 2


			#sitten kylän yläreuna
			if kylä[0]-1 >= 0:
				ylä_omistaja = omistuslauta[kylä[0]-1][kylä[1]]

				if ylä_omistaja != 2:
					ylä = True
					koko_ylä, palat_ylä = scanner(kylä[0]-1, kylä[1], lauta)

					#tarkistetaan koskettaako yksi alue ylä ja vasenta sivua
					sama_alue = False
					for pala in palat_ylä:

						#vältytään erroreilta, koska jos vasemmalla sivulla ei ole palaa ollenkaan, niin pala_vasen ei ole olemassa
						if ylä_vasen:
							if pala in palat_vasen_ylä:
								sama_alue = True
								break

						if ala_vasen:
							if pala in palat_vasen_ala:
								sama_alue = True
								break

						if ylä_oikea:
							if pala in palat_oikea_ylä:
								sama_alue = True
								break

						if ala_oikea:
							if pala in palat_oikea_ala:
								sama_alue = True
								break

					#jos ei...
					if sama_alue == False:
						#jos koko on alle 5, annetaan 1 kontrollointipiste
						if koko_ylä <5:
							if ylä_omistaja == 0:
								kontrollointipisteet_ai += 1
							else:
								kontrollointipisteet_pelaaja += 1
						#ja jos koko on yli 5 annetaan 2 kontrollointipistettä
						else:
							if ylä_omistaja == 0:
								kontrollointipisteet_ai += 2
							else:
								kontrollointipisteet_pelaaja += 2

			#sitten kylän alareuna
			if kylä[0]+1 <= 12:
				ala_omistaja = omistuslauta[kylä[0]+2][kylä[1]]

				if ala_omistaja != 2:
					koko_ala, palat_ala = scanner(kylä[0]+2, kylä[1], lauta)

					#tarkistetaan koskettaako yksi alue montaa kylän sivua
					sama_alue = False
					for pala in palat_ala:
						if ylä_vasen:
							if pala in palat_vasen_ylä:
								sama_alue = True
								break

						if ala_vasen:
							if pala in palat_vasen_ala:
								sama_alue = True
								break

						if ylä_oikea:
							if pala in palat_oikea_ylä:
								sama_alue = True
								break

						if ala_oikea:
							if pala in palat_oikea_ala:
								sama_alue = True
								break

						if ylä:
							if pala in palat_ylä:
								sama_alue = True
								break

					#jos ei...
					if sama_alue == False:
						#jos koko on alle 5, annetaan 1 kontrollointipiste
						if koko_ala <5:
							if ala_omistaja == 0:
								kontrollointipisteet_ai += 1
							else:
								kontrollointipisteet_pelaaja += 1
						#ja jos koko on yli 5 annetaan 2 kontrollointipistettä
						else:
							if ala_omistaja == 0:
								kontrollointipisteet_ai += 2
							else:
								kontrollointipisteet_pelaaja += 2


			if kontrollointipisteet_pelaaja == 0 and kontrollointipisteet_ai == 0:
				villagelauta[tuplavillaget[i][0]][tuplavillaget[i][1]] = 2

			elif kontrollointipisteet_pelaaja > kontrollointipisteet_ai:
				villagelauta[tuplavillaget[i][0]][tuplavillaget[i][1]] = 1

			elif kontrollointipisteet_ai > kontrollointipisteet_pelaaja:
				villagelauta[tuplavillaget[i][0]][tuplavillaget[i][1]] = 0



	return villagelauta


def evaluation(board,omistusboard):
	skannatut = []
	#pisteytys[0] = AI, pisteytys[1] = pelaaja
	pisteytys = [0,0]

	for i in range(len(board)):
		for j in range(len(board)):
			if [i,j] not in skannatut and board[i][j] != 0 and board[i][j] != 1:
				koko, alueen_palat = scanner(i,j,board)

				#lisätään alueen palat listaan, jottemme katso niitä enää uudestaan
				for pala in alueen_palat:
					skannatut.append(pala)

				omistaja = omistusboard[i][j]

				#if omistaja == [2,4,11]:
				#	for k in range(len(omistuslauta)):
				#		print(omistusboard[k])

				#sori fam oli pakko, ei mitään hajuu miten tää pitäs fixaa
				try:
					if koko>1 and koko<5:
						pisteytys[omistaja] += 1

					elif koko >= 5:
						pisteytys[omistaja] += 2
				except:
					pass

	#haetaan villagelauta, jossa näkyy jokaisen villagen omistajuus
	villagelauta = villagelauta_update(omistusboard,board)

	villagepisteet_ai = 0
	villagepisteet_pelaaja = 0
	#käydään läpi joka ikinen village ja riippuen sen omistajuudesta, annetaan piste sen omistajalle
	for i in range(len(villagelauta)):
		for j in range(len(villagelauta)):
			omistaja = villagelauta[i][j]
			if omistaja == 1 or omistaja == 0:
				pisteytys[omistaja] += 1

	return pisteytys





def god_move(board,y,x,suunta,pala):
	board[y][x] = int(str(pala)[0])

	if suunta == 1:
		x_2 = x+1 
		y_2 = y

	elif suunta == 2:
		x_2 = x 
		y_2 = y+1

	elif suunta == 3:
		x_2 = x-1 
		y_2 = y

	elif suunta == 4:
		x_2 = x 
		y_2 = y-1

	board[y_2][x_2] = int(str(pala)[1])

	return board


def kaikki_movet(board):
	kaikki_palat = [22,33,44,23,24,34]
	movet = []

	for pala in kaikki_palat:
		siirrot = legal_moves(pala,board)

		for siirto in siirrot:
			movet.append(siirto)

	return movet

def kaikki_movet_dumb(board):
	kaikki_palat = [22,33,44]
	movet = []

	for pala in kaikki_palat:
		siirrot = legal_moves(pala,board)

		for siirto in siirrot:
			if siirto[-2] == 1 or siirto[-2] == 2:
				movet.append(siirto)

	return movet

def ai_ekat_movet(board,ai_hand):
	movet = kaikki_movet(board)
	real_movet = []

	for move in movet:
		if move[-1] in ai_hand:
			if move[-1]==22 or move[-1]==33 or move[-1]==44:
				if move[-2]==1 or move[-2]==2:
					real_movet.append(move)
			else:
				real_movet.append(move)

	return real_movet


def random_mover(board,ai_hand):
	movet = kaikki_movet(board)
	siirto = [100,100,100,100,100]
	while siirto[-1] not in ai_hand:
		siirto = random.choice(movet)

	return siirto

def engine(v,ai_hand,lauta,omistuslauta):
	global printtaile

	positions = 0
	first = True

	if v == 0: #jos on AI vuoro

		#ENSIMMÄINEN LAYER
		maksimoitu_1 = -999 #tässä layerissä halutaan maksimoida evaluation

		kaikki_siirrot_1 = ai_ekat_movet(lauta,ai_hand) #kaikki mahdolliset AI:n siirrot (tiedetään kaikki käden kortit)

		for siirto_1 in kaikki_siirrot_1: #käydään läpi jokainen mahdollinen AI:n siirto
			new_lauta = copy.deepcopy(lauta) #kopioidaan lauta
			ai_hand_1 = copy.deepcopy(ai_hand)
			omistuslauta_1 = copy.deepcopy(omistuslauta)

			new_lauta = god_move(new_lauta,siirto_1[0],siirto_1[1],siirto_1[2],siirto_1[3]) #pelataan siirto kopioidulla laudalla

			y2,x2 = xy2(siirto_1[2],siirto_1[0],siirto_1[1])
			omistuslauta_1 = omistuslauta_update(siirto_1[3],siirto_1[0],siirto_1[1],y2,x2,new_lauta,v,omistuslauta_1,lauta) #päivitetään omistuslauta

			ai_hand_1.remove(siirto_1[3]) #poistetaan AI:n kädestä pelattu pala

			eval_1 = evaluation(lauta,omistuslauta)
			eval_2 = evaluation(new_lauta,omistuslauta_1)
			real_eval_1 = (eval_2[0]-eval_2[1])-(eval_1[0]-eval_1[1])

			#TOINEN LAYER
			minimoitu_1 = 999 #tässä layerissä halutaan minimoida evaluation
			kaikki_siirrot_2 = kaikki_movet_dumb(new_lauta) #kaikki mahdolliset siirrot mitä vastustaja voi tehdä (varaudutaan, että vastustajalla on aina paras pala kädessään)

			for siirto_2 in kaikki_siirrot_2:
				bad_move = False
				if real_eval_1 <= 0 and not first:
					bad_move = True
					break

				positions += 1

				new_lauta_2 = copy.deepcopy(new_lauta)
				omistuslauta_2 = copy.deepcopy(omistuslauta_1)

				new_lauta_2 = god_move(new_lauta_2,siirto_2[0],siirto_2[1],siirto_2[2],siirto_2[3]) #pelataan siirto kopioidulla laudalla

				y2,x2 = xy2(siirto_2[2],siirto_2[0],siirto_2[1])


				omistuslauta_2 = omistuslauta_update(siirto_2[3],siirto_2[0],siirto_2[1],y2,x2,new_lauta_2,v+1,omistuslauta_2,new_lauta) #päivitetään omistuslauta

				eval = evaluation(new_lauta_2,omistuslauta_2)
				real_eval = eval[0]-eval[1]

				if real_eval < minimoitu_1: #arviodaan lauta ja jos evaluation on pienempi, otetaan sen arvo talteen
					minimoitu_1 = real_eval


				if maksimoitu_1 >= minimoitu_1:
					break

			if minimoitu_1 > maksimoitu_1 and not bad_move:
				maksimoitu_1 = minimoitu_1
				first = False
				final_move = siirto_1 #[y,x,suunta,pala]

	print("Positions analyzed:", positions)

	return final_move







win.fill((200,200,200))
display(omistuslauta,lauta)

while True:
	if keyboard.is_pressed("q"):
		time.sleep(0.2)
		pygame.display.quit()
		pygame.quit()
		exit()

	if new:
		old_lauta = copy.deepcopy(lauta)
		new = False

	#ai vuoro
	if vuoro == 0:
		win.fill((200,200,200))
		display(omistuslauta,lauta)
		#omistuslauta = siirto(old_lauta)

		villagelauta_talteen = copy.deepcopy(villagelauta)

		start_time = time.time()
		siirto_data = engine(vuoro,ai_hand,lauta,omistuslauta)

		villagelauta = copy.deepcopy(villagelauta_talteen)

		print("TIME SPENT: "+str(round(time.time()-start_time,2))+"s")

		y = siirto_data[0]
		x = siirto_data[1]
		suunta = siirto_data[2]
		pala = siirto_data[3]

		lauta = god_move(lauta,y,x,suunta,pala)
		y2,x2 = xy2(suunta,y,x)

		omistuslauta = omistuslauta_update(pala,y,x,y2,x2,lauta,vuoro,omistuslauta,old_lauta)
		pisteet = evaluation(lauta,omistuslauta)

		new = True
		vuoro += 1

		ai_hand.remove(pala)
		uusi_pala = random.choice(pakka)
		ai_hand.append(uusi_pala)
		pakka.remove(uusi_pala)

		#optimoidaan ai nopeutta laittamalla se käymään ensin kaikki tuplat jotka sillä on kädessä
		ai_hand_temp = []
		for pala in ai_hand:
			if pala==22 or pala==33 or pala==44:
				ai_hand.remove(pala)
				ai_hand_temp.append(pala)

		for pala in ai_hand:
			ai_hand_temp.append(pala)

		ai_hand = copy.deepcopy(ai_hand_temp)

		
		win.fill((200,200,200))
		display(omistuslauta,lauta)



	#pelaajan vuoro
	elif vuoro == 1:
		omistuslauta = siirto(old_lauta)


	#villagelauta = villagelauta_update(omistuslauta,lauta)
	#for k in range(len(villagelauta)):
	#	print(villagelauta[k])

	#print("--------------------------------")
	#print(villagelauta)

	#RANDOM MOVER
	#elif vuoro == 1:
	#	data = random_mover(lauta,ai_hand_2)
	#	y = data[0]
	#	x = data[1]
	#	suunta = data[2]
	#	pala = data[3]
#
	#	lauta = god_move(lauta,y,x,suunta,pala)
	#	y2,x2 = xy2(suunta,y,x)
#
#		omistuslauta = omistuslauta_update(pala,y,x,y2,x2,lauta,vuoro,omistuslauta,old_lauta)
#		pisteet = evaluation(lauta,omistuslauta)
#
#		new = True
#		vuoro = 0
#
#		ai_hand_2.remove(pala)
#		uusi_pala = random.choice(pakka)
#		ai_hand_2.append(uusi_pala)
#		pakka.remove(uusi_pala)


