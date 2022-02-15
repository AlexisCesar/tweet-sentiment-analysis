 # -*- coding: cp932 -*-
class NaiveBayesClassifier:

    def __init__(self) -> None:
        pass

    def classify(textToClassify):
       
        print('Naive Bayes')

        WORD = 0
        POSITIVE_OCCURRENCES = 1
        NEGATIVE_OCCURRENCES = 2
        TOTAL_OCCURRENCES = 3
        POSITIVE_TENDENCY = 4
        NEGATIVE_TENDENCY = 5
        bag_of_words = list()

        SENTIMENT = 1
        training_set = [
            ['Eu odeio pizza', 'negative'],
            ['Eu odeio esse clima', 'negative'],
            ['Mds como eu amo pizza', 'positive'],
            ['Hoje é um bom dia', 'positive'],
            ['Não, isso não é bom', 'negative'],
            ['essa é uma arte legal', 'positive'],
            ['Não amigo, eu não te odeio :)', 'positive'],
            ['pizza é tudo', 'positive'],
            ['Pizza pizza pizza! <3', 'positive']
            ]

        for text in training_set:

            text_words = text[WORD].split()
            word_was_already_registered = False
            index_of_already_registered_word = -1
            print (text_words)
            
            for word in text_words:
                for registered_word in bag_of_words:
                    if word.upper() == registered_word[WORD]:
                        word_was_already_registered = True
                        index_of_already_registered_word = bag_of_words.index(registered_word)

                if word_was_already_registered == False:
                    if text[SENTIMENT] == 'positive':
                        bag_of_words.append([word.upper(), 1, 0, 1, 0, 0])
                    else:
                        bag_of_words.append([word.upper(), 0, 1, 1, 0, 0])

                else:
                    bag_of_words[index_of_already_registered_word][TOTAL_OCCURRENCES] += 1
                    
                    if text[SENTIMENT] == 'positive':
                        bag_of_words[index_of_already_registered_word][POSITIVE_OCCURRENCES] += 1
                    else:
                        bag_of_words[index_of_already_registered_word][NEGATIVE_OCCURRENCES] += 1

        # Calculating the initial guess
        positive_count = negative_count = 0
        total = len(training_set)

        for text in training_set:
            if(text[SENTIMENT] == 'positive'):
                positive_count += 1
            else:
                negative_count += 1

        positive_initial_guess = positive_count / total
        negative_initial_guess = negative_count / total

        # Add the blackbox
        for registered_word in bag_of_words:
            registered_word[POSITIVE_OCCURRENCES] += 1
            registered_word[NEGATIVE_OCCURRENCES] += 1
            registered_word[TOTAL_OCCURRENCES] += 1

        # Calculating the probability of each word
        total_positive_words_registered = total_negative_word_registered = 0
        for registered_word in bag_of_words:
            total_positive_words_registered += registered_word[POSITIVE_OCCURRENCES]
            total_negative_word_registered += registered_word[NEGATIVE_OCCURRENCES]

        for registered_word in bag_of_words:
            registered_word[POSITIVE_TENDENCY] = registered_word[POSITIVE_OCCURRENCES] / total_positive_words_registered
            registered_word[NEGATIVE_TENDENCY] = registered_word[NEGATIVE_OCCURRENCES] / total_negative_word_registered

        # Testing
        given_text = textToClassify

        positive_probability = positive_initial_guess
        negative_probability = negative_initial_guess

        for word in given_text.upper().split():
            for registered_word in bag_of_words:
                if word == registered_word[WORD]:
                    positive_probability = positive_probability * registered_word[POSITIVE_TENDENCY]
                    negative_probability = negative_probability * registered_word[NEGATIVE_TENDENCY]

        classification = 'neutral'

        if positive_probability > negative_probability:
            classification = 'positive'
        elif negative_probability > positive_probability:
            classification = 'negative'

        print(given_text, " - Classification: ", classification)
