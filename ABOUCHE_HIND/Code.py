# ******************** créer par *************************
#**************** HIND ABOUCHE *************************
#**************BIG DATA*******************************
#***********2020************************************
import tweepy,csv,re
from textblob import TextBlob
import matplotlib.pyplot as pl
class SentimentAnalysis:
    def __init__(self):
        self.tweets = []
        self.tweetText = []
    def get_tweets(self):
        consumerKey = "WDnCulflaJEnf7YYHl7N5HMMP"
        consumerSecret = "ZV5YDgbaG9aaN3QbXt1nHjYTLKBtFBfAqDawOG2w9veECt6AML"
        accessToken = "1270269131506548736-EDwf471vKNQ7U1sEU1PhJJYffNJ0qU"
        accessTokenSecret = "WAoIYtbTjX1U01GksxmcIdTAtqAglhH5MAWkMixXgfCwf"
        #etablir la connection avec our API
        auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
        auth.set_access_token(accessToken, accessTokenSecret)
        api = tweepy.API(auth)

        # donner la main à l'utilisateur pour choisir le mot et le nombre de Hashtag
        tag = input("Saisissez un tag pour rechercher SVP :")
        nb_tweets = int(input("Entrez le nombre de tweets à rechercher SVP: "))

        # rechercher sur les tweets  en anglais
        self.tweets = tweepy.Cursor(api.search, q=tag, lang = "en").items(nb_tweets)

        # Ouvrir un fichier csv pour ajouter les datas
        csv_file = open('Tweets.csv', 'a')

        # Utiliser csv.writer
        csvWriter = csv.writer(csv_file)


        # creation des nv variables pour stockers les infos
        polarity = 0
        positive = 0
        negative = 0
        neutral = 0


        # itération à travers des tweets récupérés
        for tweet in self.tweets:
            #Ajoutez à temp pour que nous puissions stocker dans csv plus tard. (encoder UTF-8)
            #appeler à la fonction cleanTweet
            self.tweetText.append(self.cleanTweet(tweet.text).encode('utf-8'))
            #print tweet's text
            analysis = TextBlob(tweet.text)
            polarity += analysis.sentiment.polarity  # additionner les polarités pour trouver la moyenne plus tard
            # ajouter une réaction sur la façon dont les gens réagissent pour trouver la moyenne
            if (analysis.sentiment.polarity == 0):
                neutral += 1
            elif (analysis.sentiment.polarity > 0):
                positive += 1
            elif (analysis.sentiment.polarity <0):
                negative += 1


        # ecrire dans le fichier csv et fermer le fichier
        csvWriter.writerow(self.tweetText)
        csv_file.close()


        # trouver la moyenne de la réaction des gens
        positive = self.percentage(positive, nb_tweets)
        negative = self.percentage(negative, nb_tweets)
        neutral = self.percentage(neutral, nb_tweets)

        #
        # trouver une réaction moyenne
        polarity = polarity / nb_tweets

        # affichage de notre data
        print("Comment les gens réagissent à " + tag + " en analysant  " + str(nb_tweets) + " tweets.")

        if (polarity == 0):
            print("Neutral")
        elif (polarity > 0):
            print("Positive")
        elif (polarity <0):
            print("Negative")

        print()
        print(str(positive) + "% des gens pensaient que c'était positif")
        print(str(negative) + "% des gens pensaient que c'était negative")
        print(str(neutral) + "% des gens pensaient que c'était neutral")
        #appeler à la fonction plot()
        self.plot(positive,negative,neutral, tag, nb_tweets)


    def cleanTweet(self, tweet):
        # Supprimer les liens, les caractères spéciaux, etc. du tweet
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) | (\w +:\ / \ / \S +)", " ", tweet).split())

    # fonction pour calculer le pourcentage
    def percentage(self, part, whole):
        temp = 100 * float(part) / float(whole)
        return format(temp, '.2f')

    def plot(self, positive, negative, neutral, tag, nb_tweets):
        labels = ['Positive [' + str(positive) + '%]', 'Neutral [' + str(neutral) + '%]',
                  'Negative [' + str(negative) + '%]']
        sizes = [positive, neutral, negative]
        colors = ['blue', 'gold', 'red']
        patches, texts = plt.pie(sizes, colors=colors, startangle=90)
        plt.legend(patches, labels, loc="best")
        plt.title('Comment les gens réagissent à ' + tag + ' en analysant  ' + str(nb_tweets) + ' Tweets.')
        plt.axis('equal')
        plt.tight_layout()
        plt.show()



if __name__== "__main__":
    sa = SentimentAnalysis()
    sa.get_tweets()
