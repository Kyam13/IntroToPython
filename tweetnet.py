import sys, os
import pyhum.preprocess

TWITTERDATA = './data/twitterdata'

class Tweet:
    def __init__(self, message, time):
        self.message = message
        self.time = time

class TwitterUser:
    def __init__(self, name):
        self.name = name
        self.tweets = [] #This will be a list of all tweets
        self.relations = {} #This will be a dictionary in which the keys are user names and
                            #the values are the weight of the relation (an integer)

    def append(self, tweet):
        assert isinstance(tweet, Tweet) #this is a test, if tweet is not an instance
                                        #of Tweet, it will raise an Exception.
        self.tweets.append(tweet)

    def __iter__(self):
        #This function, a generator, should iterate over all tweets
        #<INSERT YOUR CODE HERE>
        for tweet in sorted(self.tweets):
            yield tweet


    def __hash__(self):
        #For an object to be usable as a dictionary key, it must have a hash method.
        #Call the hash() function over something that uniquely defined this object
        #and thus can act as a key in a dictionary. In our case, the user name is good,
        #as no two users will have the same name:
        return hash(self.name)


    def addrelation(self, user):
        if user and user != self.name: #user must not be empty, and must not be the user itself
            if user in self.relations:
                #the user is already in our relations, strengthen the bond:
                self.relations[user] += 1
            else :
                #we add a relation!
                self.relations[user] = 1


    def computerelations(self):
        pass
        #for tweet in self.tweets:
            #tokenise the actual tweet content (use the tokeniser in preprocess!):
            #<INSERT YOUR CODE HERE>
            #tokenstweet=pyhum.preprocess.tokenise(tweet)
            #sentences=pyhum.preprocess.split_sentences(tokenstweet)
            #Search for @username tokens, extract the username, and call self.addrelation()
            #<INSERT YOUR CODE HERE>
            #for s in sentences:
            #    if s[0]=="@":
            #        self.addrelation(s)


    def printrelations(self):
        pass
        #print the relations, include both users and the weight
        #<INSERT YOUR CODE HERE>
        #print(self.relations)


    def output(self):
        #produce CSV output
        for recipient, weight in self.relations.items():
            yield self.name + "," + recipient + "," + str(weight)

#すべてのtwitterユーザーを格納する辞書の初期化。これらのキーはユーザー名（文字列）であり、値はTweetUserインスタンス
#ツイッターコーパスを読み込む
#tip：preprocess.find_corpus_filesとpreprocess.read_corpus_fileを使用してください。
#preproces.readcorpusを使用しないでください。これは、望ましくない文のセグメンテーションが含まれるためです
#各txtファイルには、1人のユーザーのつぶやきが含まれています。すべてのファイルには、
#TAB（\ t）で区切られた3つの列があります。最初の列はユーザ​​ー、2番目は時間、3番目はツイートメッセージそのものです。
# @を含むすべての行に対してTweetインスタンスを作成します（他のlinesto節約メモリは無視します）。
#これらのツイートインスタンスを右のTweetUserに追加します。新しいユーザが遭遇したときにTweetUserインスタンスを作成します.
#self.users [ユーザ]はユーザ名（文字列）で、TweetUserのインスタンスにする必要があります

class TwitterGraph:
    def __init__(self, corpusdirectory):
        self.users = {} #initialisation of dictionary that will store all twitter users.
                        #the keys are the usernames (strings), and the values are
                        # TweetUser instances

        #Load the twitter corpus
        #tip: use preprocess.find_corpus_files and preprocess.read_corpus_file,
        #do not use preproces.readcorpus as that will include sentence segmentation
        #which we do not want


        #Each txt file contains the tweets of one user.
        #all files contain three columns, separated by a TAB (\t). The first column
        #is the user, the second the time, and the third is the tweetmessage itself.
        #Create Tweet instances for every line that contains a @ (ignore other lines
        #to conserve memory). Add those tweet instances to the right TweetUser. Create
        #TweetUser instances as new users are encountered.

        #self.users[user], which user being the username (string), should be an instance of the
        #of TweetUser

        #<INSERT YOUR CODE HERE>
        words=[]
        words2=[]
        cnt=1
        for filepath in pyhum.preprocess.find_corpus_files (corpusdirectory):
            text=pyhum.preprocess.read_corpus_file(filepath)
            words2=text.split("\n")
            text2='\t'.join(words2)
            words=text2.split("\t")
            tweeter=TwitterUser(words[0])
            self.users[words[0]]=tweeter
            for i,txt in enumerate(words):
                if i==3*cnt-1:
                    tweeter.append(txt)
                    cnt+=1

            words=[]
            words2=[]
            cnt=1
            #print("words[2]\t",words[2])   words[2,5,...] is tweet
        #Compute relations between users
        for user in self.users.values():
            assert isinstance(user,TwitterUser)
            user.computerelations()

# cnt 1536        print(cnt)

    def __contains__(self, user):
        #Does this user exist?
        return user in self.users

    def __iter__(self):
        #Iterate over all users
        for user in self.users.values():
            yield user

    def __getitem__(self, user):
        #Retrieve the specified user
        return self.users[user]


#this is the actual main body of the program.

#We instantiate the graph, which will load and compute all relations
twittergraph = TwitterGraph(TWITTERDATA)

#We can output all relations, but don't do it here because it will produce very long
#list (more than 100,000) of relations.
#for twitteruser in twittergraph:
#    twitteruser.printrelations()

#It is betterto output relations to a file, Check the contents of this file!
f = open('graph.csv','wt',encoding='utf-8')
for twitteruser in twittergraph:
    for line in twitteruser.output():
        f.write(line + "\n")
f.close()


# do no change these lines. They are for check whether your script works
print (len(twittergraph.users))#==1537)
print (max([len(user.relations) for user in twittergraph]))#==2606)
