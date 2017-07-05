#!/usr/bin/python 
#
# wget wget http://www2.imm.dtu.dk/pubdb/views/edoc_download.php/6010/zip/imm6010.zip
# unzip imm6010.zip

import math
import re
import sys
from pymongo import MongoClient
import datetime
import nltk
import time
import matplotlib.pyplot as plt
from nltk import *

reload(sys)
sys.setdefaultencoding('utf-8')

#Open a connection to MongoDb (localhost)
client=MongoClient("localhost", 27017)
db = client.twitter


# word list is as of December 2011 
filenameWords = 'words/wordweightings.txt'
wordlist = dict(map(lambda (w, s): (w, int(s)), [
            ws.strip().split('\t') for ws in open(filenameWords) ]))
o1 = open("output_final.txt","wb+")

# Word splitter pattern
pattern_split = re.compile(r"\W+")

def sentiment(text):

    neg_tweets = [("it's so laddish and juvenile , only teenage boys could possibly find it funny .", 'negative'),
    ('exploitative and largely devoid of the depth or sophistication that would make watching such a graphic treatment of the crimes bearable .', 'negative'),
    ('[garbus] discards the potential for pathological study , exhuming instead , the skewed melodrama of the circumstantial situation .', 'negative'),
    ('a visually flashy but narratively opaque and emotionally vapid exercise in style and mystification .', 'negative'),
    ("the story is also as unoriginal as they come , already having been recycled more times than i'd care to count .", 'negative'),
    ("about the only thing to give the movie points for is bravado -- to take an entirely stale concept and push it through the audience's meat grinder one more time .", 'negative'),
    ('not so much farcical as sour .', 'negative'),
    ('unfortunately the story and the actors are served with a hack script .', 'negative'),
    ('all the more disquieting for its relatively gore-free allusions to the serial murders , but it falls down in its attempts to humanize its subject .', 'negative'),
    ('a sentimental mess that never rings true .', 'negative'),
    ('while the performances are often engaging , this loose collection of largely improvised numbers would probably have worked better as a one-hour tv documentary .', 'negative'),
    ('interesting , but not compelling .', 'negative'),
    ('on a cutting room floor somewhere lies . . . footage that might have made no such thing a trenchant , ironic cultural satire instead of a frustrating misfire .', 'negative'),
    ("while the ensemble player who gained notice in guy ritchie's lock , stock and two smoking barrels and snatch has the bod , he's unlikely to become a household name on the basis of his first starring vehicle .", 'negative'),
    ("there is a difference between movies with the courage to go over the top and movies that don't care about being stupid", 'negative'),
    ("nothing here seems as funny as it did in analyze this , not even joe viterelli as de niro's right-hand goombah .", 'negative'),
    ('such master screenwriting comes courtesy of john pogue , the yale grad who previously gave us " the skulls " and last year\'s " rollerball . " enough said , except : film overboard !', 'negative'),
    ('here , common sense flies out the window , along with the hail of bullets , none of which ever seem to hit sascha .', 'negative'),
    ('this 100-minute movie only has about 25 minutes of decent material .', 'negative'),
    ('the execution is so pedestrian that the most positive comment we can make is that rob schneider actually turns in a pretty convincing performance as a prissy teenage girl .', 'negative'),
    ("on its own , it's not very interesting . as a remake , it's a pale imitation .", 'negative'),
    ("it shows that some studios firmly believe that people have lost the ability to think and will forgive any shoddy product as long as there's a little girl-on-girl action .", 'negative'),
    ("a farce of a parody of a comedy of a premise , it isn't a comparison to reality so much as it is a commentary about our knowledge of films .", 'negative'),
    ('as exciting as all this exoticism might sound to the typical pax viewer , the rest of us will be lulled into a coma .', 'negative'),
    ('the party scenes deliver some tawdry kicks . the rest of the film . . . is dudsville .', 'negative'),
    ("our culture is headed down the toilet with the ferocity of a frozen burrito after an all-night tequila bender \x97 and i know this because i've seen 'jackass : the movie . '", 'negative'),
    ('the criticism never rises above easy , cynical potshots at morally bankrupt characters . . .', 'negative'),
    ("the movie's something-borrowed construction feels less the product of loving , well integrated homage and more like a mere excuse for the wan , thinly sketched story . killing time , that's all that's going on here .", 'negative'),
    ('stupid , infantile , redundant , sloppy , over-the-top , and amateurish . yep , it\'s " waking up in reno . " go back to sleep .', 'negative'),
    ('somewhere in the middle , the film compels , as demme experiments he harvests a few movie moment gems , but the field of roughage dominates .', 'negative'),
    ('the action clich\xe9s just pile up .', 'negative'),
    ("payami tries to raise some serious issues about iran's electoral process , but the result is a film that's about as subtle as a party political broadcast .", 'negative'),
    ("the only surprise is that heavyweights joel silver and robert zemeckis agreed to produce this ; i assume the director has pictures of them cavorting in ladies' underwear .", 'negative'),
    ("another useless recycling of a brutal mid-'70s american sports movie .", 'negative'),
    ("i didn't laugh . i didn't smile . i survived .", 'negative'),
    ('please , someone , stop eric schaeffer before he makes another film .', 'negative'),
    ("most of the problems with the film don't derive from the screenplay , but rather the mediocre performances by most of the actors involved", 'negative'),
    (". . . if you're just in the mood for a fun -- but bad -- movie , you might want to catch freaks as a matinee .", 'negative'),
    ('curling may be a unique sport but men with brooms is distinctly ordinary .', 'negative'),
    ('though the opera itself takes place mostly indoors , jacquot seems unsure of how to evoke any sort of naturalism on the set .', 'negative'),
    ("there's no getting around the fact that this is revenge of the nerds revisited -- again .", 'negative'),
    ("the effort is sincere and the results are honest , but the film is so bleak that it's hardly watchable .", 'negative'),
    ("analyze that regurgitates and waters down many of the previous film's successes , with a few new swings thrown in .", 'negative'),
    ("with flashbulb editing as cover for the absence of narrative continuity , undisputed is nearly incoherent , an excuse to get to the closing bout . . . by which time it's impossible to care who wins .", 'negative'),
    ('stinks from start to finish , like a wet burlap sack of gloom .', 'negative'),
    ('to the civilized mind , a movie like ballistic : ecks vs . sever is more of an ordeal than an amusement .', 'negative'),
    ("equlibrium could pass for a thirteen-year-old's book report on the totalitarian themes of 1984 and farenheit 451 .", 'negative'),
    ("the lack of naturalness makes everything seem self-consciously poetic and forced . . . it's a pity that [nelson's] achievement doesn't match his ambition .", 'negative'),
    ('everything is off .', 'negative'),
    ("when seagal appeared in an orange prison jumpsuit , i wanted to stand up in the theater and shout , 'hey , kool-aid ! '", 'negative'),
    ('an easy watch , except for the annoying demeanour of its lead character .', 'negative'),
    ("imagine the cleanflicks version of 'love story , ' with ali macgraw's profanities replaced by romance-novel platitudes .", 'negative'),
    ('pc stability notwithstanding , the film suffers from a simplistic narrative and a pat , fairy-tale conclusion .', 'negative'),
    ("forget the misleading title , what's with the unexplained baboon cameo ?", 'negative'),
    ('an odd , haphazard , and inconsequential romantic comedy .', 'negative'),
    ('though her fans will assuredly have their funny bones tickled , others will find their humor-seeking dollars best spent elsewhere .', 'negative'),
    ("pascale bailly's rom-com provides am\xe9lie's audrey tautou with another fabuleux destin -- i . e . , a banal spiritual quest .", 'negative'),
    ('a static and sugary little half-hour , after-school special about interfaith understanding , stretched out to 90 minutes .', 'negative'),
    ('watching the chemistry between freeman and judd , however , almost makes this movie worth seeing . almost .', 'negative'),
    ('. . . a pretentious and ultimately empty examination of a sick and evil woman .', 'negative'),
    ('the country bears has no scenes that will upset or frighten young viewers . unfortunately , there is almost nothing in this flat effort that will amuse or entertain them , either .', 'negative'),
    ("the cumulative effect of watching this 65-minute trifle is rather like being trapped while some weird relative trots out the video he took of the family vacation to stonehenge . before long , you're desperate for the evening to end .", 'negative'),
    ('the characters are never more than sketches . . . which leaves any true emotional connection or identification frustratingly out of reach .', 'negative'),
    ("mattei's underdeveloped effort here is nothing but a convenient conveyor belt of brooding personalities that parade about as if they were coming back from stock character camp -- a drowsy drama infatuated by its own pretentious self-examination .", 'negative'),
    ("only in its final surprising shots does rabbit-proof fence find the authority it's looking for .", 'negative'),
    ("isn't as sharp as the original . . . despite some visual virtues , 'blade ii' just doesn't cut it .", 'negative'),
    (". . . plays like a badly edited , 91-minute trailer ( and ) the director can't seem to get a coherent rhythm going . in fact , it doesn't even seem like she tried .", 'negative'),
    ('maybe leblanc thought , " hey , the movie about the baseball-playing monkey was worse . "', 'negative'),
    ("what you expect is just what you get . . . assuming the bar of expectations hasn't been raised above sixth-grade height .", 'negative'),
    ('barry sonnenfeld owes frank the pug big time', 'negative'),
    ("the biggest problem with roger avary's uproar against the mpaa is that , even in all its director's cut glory , he's made a film that's barely shocking , barely interesting and most of all , barely anything .", 'negative'),
    ('so riddled with unanswered questions that it requires gargantuan leaps of faith just to watch it plod along .', 'negative'),
    ('i approached the usher and said that if she had to sit through it again , she should ask for a raise .', 'negative'),
    ('earnest but heavy-handed .', 'negative'),
    ("if sinise's character had a brain his ordeal would be over in five minutes but instead the plot goes out of its way to introduce obstacles for him to stumble over .", 'negative'),
    ('too slow for a younger crowd , too shallow for an older one .', 'negative'),
    ('there\'s a reason the studio didn\'t offer an advance screening . " the adventures of pluto nash " is a big time stinker .', 'negative'),
    ('a punch line without a premise , a joke built entirely from musty memories of half-dimensional characters .', 'negative'),
    ("takes one character we don't like and another we don't believe , and puts them into a battle of wills that is impossible to care about and isn't very funny .", 'negative'),
    ("the things this movie tries to get the audience to buy just won't fly with most intelligent viewers .", 'negative'),
    ("even if the enticing prospect of a lot of nubile young actors in a film about campus depravity didn't fade amid the deliberate , tiresome ugliness , it would be rendered tedious by avary's failure to construct a story with even a trace of dramatic interest .", 'negative'),
    ('sitting through the last reel ( spoiler alert ! ) is significantly less charming than listening to a four-year-old with a taste for exaggeration recount his halloween trip to the haunted house .', 'negative'),
    ('confuses its message with an ultimate desire to please , and contorting itself into an idea of expectation is the last thing any of these three actresses , nor their characters , deserve .', 'negative'),
    ('deadly dull , pointless meditation on losers in a gone-to-seed hotel .', 'negative'),
    ('with this new rollerball , sense and sensibility have been overrun by what can only be characterized as robotic sentiment .', 'negative'),
    ("one can only assume that the jury who bestowed star hoffman's brother gordy with the waldo salt screenwriting award at 2002's sundance festival were honoring an attempt to do something different over actually pulling it off", 'negative'),
    ("a movie more to be prescribed than recommended -- as visually bland as a dentist's waiting room , complete with soothing muzak and a cushion of predictable narrative rhythms .", 'negative'),
    ('sex ironically has little to do with the story , which becomes something about how lame it is to try and evade your responsibilities and that you should never , ever , leave a large dog alone with a toddler . but never mind all that ; the boobs are fantasti', 'negative'),
    ("the script covers huge , heavy topics in a bland , surfacey way that doesn't offer any insight into why , for instance , good things happen to bad people .", 'negative'),
    ('a portrait of alienation so perfect , it will certainly succeed in alienating most viewers .', 'negative'),
    ('the code talkers deserved better than a hollow tribute .', 'negative'),
    ('skip the film and buy the philip glass soundtrack cd .', 'negative'),
    ('feels like a cold old man going through the motions .', 'negative'),
    ("dignified ceo's meet at a rustic retreat and pee against a tree . can you bear the laughter ?", 'negative'),
    ('dull and mechanical , kinda like a very goofy museum exhibit', 'negative'),
    ("there's no point of view , no contemporary interpretation of joan's prefeminist plight , so we're left thinking the only reason to make the movie is because present standards allow for plenty of nudity .", 'negative'),
    ('beware the quirky brit-com . they can and will turn on a dime from oddly humorous to tediously sentimental .', 'negative'),
    ('has its moments -- and almost as many subplots .', 'negative'),
    ('the gags , and the script , are a mixed bag .', 'negative'),
    ('completely awful iranian drama . . . as much fun as a grouchy ayatollah in a cold mosque .', 'negative'),
    ('narratively , trouble every day is a plodding mess .', 'negative')
    ]
    
    pos_tweets = [('the rock is destined to be the 21st century\'s new " conan " and that he\'s going to make a splash even greater than arnold schwarzenegger , jean-claud van damme or steven segal .', 'positive'),
    ('the gorgeously elaborate continuation of " the lord of the rings " trilogy is so huge that a column of words cannot adequately describe co-writer/director peter jackson\'s expanded vision of j . r . r . tolkien\'s middle-earth .', 'positive'),
    ('effective but too-tepid biopic', 'positive'),
    ('if you sometimes like to go to the movies to have fun , wasabi is a good place to start .', 'positive'),
    ("emerges as something rare , an issue movie that's so honest and keenly observed that it doesn't feel like one .", 'positive'),
    ('the film provides some great insight into the neurotic mindset of all comics -- even those who have reached the absolute top of the game .', 'positive'),
    ('offers that rare combination of entertainment and education .', 'positive'),
    ('perhaps no picture ever made has more literally showed that the road to hell is paved with good intentions .', 'positive'),
    ("steers turns in a snappy screenplay that curls at the edges ; it's so clever you want to hate it . but he somehow pulls it off .", 'positive'),
    ('take care of my cat offers a refreshingly different slice of asian cinema .', 'positive'),
    ('this is a film well worth seeing , talking and singing heads and all .', 'positive'),
    ('what really surprises about wisegirls is its low-key quality and genuine tenderness .', 'positive'),
    ('( wendigo is ) why we go to the cinema : to be fed through the eye , the heart , the mind .', 'positive'),
    ('one of the greatest family-oriented , fantasy-adventure movies ever .', 'positive'),
    ('ultimately , it ponders the reasons we need stories so much .', 'positive'),
    ("an utterly compelling 'who wrote it' in which the reputation of the most famous author who ever lived comes into question .", 'positive'),
    ('illuminating if overly talky documentary .', 'positive'),
    ('a masterpiece four years in the making .', 'positive'),
    ("the movie's ripe , enrapturing beauty will tempt those willing to probe its inscrutable mysteries .", 'positive'),
    ('offers a breath of the fresh air of true sophistication .', 'positive'),
    ('a thoughtful , provocative , insistently humanizing film .', 'positive'),
    ('with a cast that includes some of the top actors working in independent film , lovely & amazing involves us because it is so incisive , so bleakly amusing about how we go about our lives .', 'positive'),
    ('a disturbing and frighteningly evocative assembly of imagery and hypnotic music composed by philip glass .', 'positive'),
    ("not for everyone , but for those with whom it will connect , it's a nice departure from standard moviegoing fare .", 'positive'),
    ('scores a few points for doing what it does with a dedicated and good-hearted professionalism .', 'positive'),
    ("occasionally melodramatic , it's also extremely effective .", 'positive'),
    ('spiderman rocks', 'positive'),
    ('an idealistic love story that brings out the latent 15-year-old romantic in everyone .', 'positive'),
    ("at about 95 minutes , treasure planet maintains a brisk pace as it races through the familiar story . however , it lacks grandeur and that epic quality often associated with stevenson's tale as well as with earlier disney efforts .", 'positive'),
    ('it helps that lil bow wow . . . tones down his pint-sized gangsta act to play someone who resembles a real kid .', 'positive'),
    ('guaranteed to move anyone who ever shook , rattled , or rolled .', 'positive'),
    ('a masterful film from a master filmmaker , unique in its deceptive grimness , compelling in its fatalist worldview .', 'positive'),
    ('light , cute and forgettable .', 'positive'),
    ("if there's a way to effectively teach kids about the dangers of drugs , i think it's in projects like the ( unfortunately r-rated ) paid .", 'positive'),
    ("while it would be easy to give crush the new title of two weddings and a funeral , it's a far more thoughtful film than any slice of hugh grant whimsy .", 'positive'),
    ('though everything might be literate and smart , it never took off and always seemed static .', 'positive'),
    ("cantet perfectly captures the hotel lobbies , two-lane highways , and roadside cafes that permeate vincent's days", 'positive'),
    ('ms . fulford-wierzbicki is almost spooky in her sulky , calculating lolita turn .', 'positive'),
    ('though it is by no means his best work , laissez-passer is a distinguished and distinctive effort by a bona-fide master , a fascinating film replete with rewards to be had by all willing to make the effort to reap them .', 'positive'),
    ('like most bond outings in recent years , some of the stunts are so outlandish that they border on being cartoonlike . a heavy reliance on cgi technology is beginning to creep into the series .', 'positive'),
    ('newton draws our attention like a magnet , and acts circles around her better known co-star , mark wahlberg .', 'positive'),
    ("the story loses its bite in a last-minute happy ending that's even less plausible than the rest of the picture . much of the way , though , this is a refreshingly novel ride .", 'positive'),
    ('fuller would surely have called this gutsy and at times exhilarating movie a great yarn .', 'positive'),
    ("'compleja e intelectualmente retadora , el ladr\xf3n de orqu\xeddeas es uno de esos filmes que vale la pena ver precisamente por su originalidad . '", 'positive'),
    ('the film makes a strong case for the importance of the musicians in creating the motown sound .', 'positive'),
    ('karmen moves like rhythm itself , her lips chanting to the beat , her long , braided hair doing little to wipe away the jeweled beads of sweat .', 'positive'),
    ('gosling provides an amazing performance that dwarfs everything else in the film .', 'positive'),
    ("a real movie , about real people , that gives us a rare glimpse into a culture most of us don't know .", 'positive'),
    ('tender yet lacerating and darkly funny fable .', 'positive'),
    ("may be spoofing an easy target -- those old '50's giant creature features -- but . . . it acknowledges and celebrates their cheesiness as the reason why people get a kick out of watching them today .", 'positive'),
    ("an engaging overview of johnson's eccentric career .", 'positive'),
    ('in its ragged , cheap and unassuming way , the movie works .', 'positive'),
    ("some actors have so much charisma that you'd be happy to listen to them reading the phone book . hugh grant and sandra bullock are two such likeable actors .", 'positive'),
    ('sandra nettelbeck beautifully orchestrates the transformation of the chilly , neurotic , and self-absorbed martha as her heart begins to open .', 'positive'),
    ('behind the snow games and lovable siberian huskies ( plus one sheep dog ) , the picture hosts a parka-wrapped dose of heart .', 'positive'),
    ('everytime you think undercover brother has run out of steam , it finds a new way to surprise and amuse .', 'positive'),
    ('manages to be original , even though it rips off many of its ideas .', 'positive'),
    ('singer/composer bryan adams contributes a slew of songs \x97 a few potential hits , a few more simply intrusive to the story \x97 but the whole package certainly captures the intended , er , spirit of the piece .', 'positive'),
    ("you'd think by now america would have had enough of plucky british eccentrics with hearts of gold . yet the act is still charming here .", 'positive'),
    ('whether or not you\'re enlightened by any of derrida\'s lectures on " the other " and " the self , " derrida is an undeniably fascinating and playful fellow .', 'positive'),
    ('a pleasant enough movie , held together by skilled ensemble actors .', 'positive'),
    ("this is the best american movie about troubled teens since 1998's whatever .", 'positive'),
    ("disney has always been hit-or-miss when bringing beloved kids' books to the screen . . . tuck everlasting is a little of both .", 'positive'),
    ('just the labour involved in creating the layered richness of the imagery in this chiaroscuro of madness and light is astonishing .', 'positive'),
    ('the animated subplot keenly depicts the inner struggles of our adolescent heroes - insecure , uncontrolled , and intense .', 'positive'),
    ('the invincible werner herzog is alive and well and living in la', 'positive'),
    ('morton is a great actress portraying a complex character , but morvern callar grows less compelling the farther it meanders from its shocking start .', 'positive'),
    ('part of the charm of satin rouge is that it avoids the obvious with humour and lightness .', 'positive'),
    ('son of the bride may be a good half-hour too long but comes replete with a flattering sense of mystery and quietness .', 'positive'),
    ('a simmering psychological drama in which the bursts of sudden violence are all the more startling for the slow buildup that has preceded them .', 'positive'),
    ('a taut , intelligent psychological drama .', 'positive'),
    ("a compelling coming-of-age drama about the arduous journey of a sensitive young girl through a series of foster homes and a fierce struggle to pull free from her dangerous and domineering mother's hold over her .", 'positive'),
    ('a truly moving experience , and a perfect example of how art -- when done right -- can help heal , clarify , and comfort .', 'positive'),
    ('this delicately observed story , deeply felt and masterfully stylized , is a triumph for its maverick director .', 'positive'),
    ('at heart the movie is a deftly wrought suspense yarn whose richer shadings work as coloring rather than substance .', 'positive'),
    ("the appearance of treebeard and gollum's expanded role will either have you loving what you're seeing , or rolling your eyes . i loved it ! gollum's 'performance' is incredible !", 'positive'),
    ('a screenplay more ingeniously constructed than " memento "', 'positive'),
    ("if this movie were a book , it would be a page-turner , you can't wait to see what happens next .", 'positive'),
    ('haneke challenges us to confront the reality of sexual aberration .', 'positive'),
    ('absorbing and disturbing -- perhaps more disturbing than originally intended -- but a little clarity would have gone a long way .', 'positive'),
    ("it's the best film of the year so far , the benchmark against which all other best picture contenders should be measured .", 'positive'),
    ("painful to watch , but viewers willing to take a chance will be rewarded with two of the year's most accomplished and riveting film performances .", 'positive'),
    ('this is a startling film that gives you a fascinating , albeit depressing view of iranian rural life close to the iraqi border .', 'positive'),
    ('an imaginative comedy/thriller .', 'positive'),
    ('a few artsy flourishes aside , narc is as gritty as a movie gets these days .', 'positive'),
    ('while the isle is both preposterous and thoroughly misogynistic , its vistas are incredibly beautiful to look at .', 'positive'),
    ("together , tok and o orchestrate a buoyant , darkly funny dance of death . in the process , they demonstrate that there's still a lot of life in hong kong cinema .", 'positive'),
    ('director kapur is a filmmaker with a real flair for epic landscapes and adventure , and this is a better film than his earlier english-language movie , the overpraised elizabeth .', 'positive'),
    ('the movie is a blast of educational energy , as bouncy animation and catchy songs escort you through the entire 85 minutes .', 'positive'),
    ("a sports movie with action that's exciting on the field and a story you care about off it .", 'positive'),
    ("doug liman , the director of bourne , directs the traffic well , gets a nice wintry look from his locations , absorbs us with the movie's spycraft and uses damon's ability to be focused and sincere .", 'positive'),
    ('the tenderness of the piece is still intact .', 'positive'),
    ('katz uses archival footage , horrifying documents of lynchings , still photographs and charming old reel-to-reel recordings of meeropol entertaining his children to create his song history , but most powerful of all is the song itself', 'positive'),
    ("like the film's almost anthropologically detailed realization of early-'80s suburbia , it's significant without being overstated .", 'positive'),
    ("while mcfarlane's animation lifts the film firmly above the level of other coming-of-age films . . . it's also so jarring that it's hard to get back into the boys' story .", 'positive'),
    ('if nothing else , this movie introduces a promising , unusual kind of psychological horror .', 'positive'),
    ('in a normal screen process , these bromides would be barely enough to sustain an interstitial program on the discovery channel . but in imax 3-d , the clich\xe9s disappear into the vertiginous perspectives opened up by the photography .', 'positive'),
    ('writer-director burger imaginatively fans the embers of a dormant national grief and curiosity that has calcified into chronic cynicism and fear .', 'positive'),
    ('. . . a roller-coaster ride of a movie', 'positive'),
    ('i enjoyed time of favor while i was watching it , but i was surprised at how quickly it faded from my memory .', 'positive'),
    ('chicago is sophisticated , brash , sardonic , completely joyful in its execution .', 'positive')
    ]
    
    tweets = []
    for (words, sentiment) in neg_tweets + pos_tweets:
	words_filtered = [e.lower() for e in words.split() if len(e) >= 3] 
	tweets.append((words_filtered, sentiment))
#    print '\n'
    def get_words_in_tweets(tweets):
	    all_words = []
	    for (words, sentiment) in tweets:
		    all_words.extend(words)
#	    print '\n'
    #	print all_words
#	    print '\n'
	    return all_words

    def get_word_features(wordlist):
	    wordlist = nltk.FreqDist(wordlist)
	    word_features = wordlist.keys()
#	    print '\n'
    #	print word_features
#	    print '\n'
	    return word_features
    word_features = get_word_features(get_words_in_tweets(tweets))
    #print word_features
    #The Classifier

    def extract_features(document):
	document_words = set(document)
	features = {}
	for word in word_features:
	    features['contains(%s)' % word] = (word in document_words)
	return features

    training_set = nltk.classify.apply_features(extract_features, tweets)
#   print '\n'
    #print training_set
#    print '\n'
    #print '\nAccuracy %f\n' % nltk.classify.accuracy(classifier, training_set)
    



    classifier = nltk.NaiveBayesClassifier.train(training_set)

    def train(labeled_featuresets, estimator=nltk.probability.ELEProbDist):
	    label_probdist = estimator(label_freqdist)
	    feature_probdist = {}
	    return NaiveBayesClassifier(label_probdist, feature_probdist)

    #res = classifier.classify(extract_features(text.split()))
    print str(text + ": " + classifier.classify(extract_features(text.split())))
    o1.write(str(text + ": " + classifier.classify(extract_features(text.split()))) + "\n")
      
    #print '\nAccuracy %f\n' % nltk.classify.accuracy(classifier, training_set)
    #print '\nAccuracy-Tweets %f\n' % nltk.classify.accuracy(classifier, tweets)

if __name__ == '__main__':
    # Get the records from Mongo
    records = db.streaming.find()
    sentiments = map(sentiment, [ tweet['text'] for tweet in records ])
    #db.sentiment.insert({'sentiment': "%6.2f" % (sum(sentiments)/math.sqrt(len(sentiments))), 'date': datetime.datetime.utcnow()})
    #db.sentiment.insert({sentiment})
    #print("%6.2f" % (sum(sentiments)/math.sqrt(len(sentiments))))
    
