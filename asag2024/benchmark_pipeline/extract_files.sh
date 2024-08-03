mkdir -p $PWD/data/original

# TODO: These pathes should be coming from the central configuration
unzip $PWD/data/compressed/semeval-5way.zip -d $PWD/data/original/semeval-5way

tar -xf $PWD/data/compressed/Mohler_ShortAnswerGrading_v1.0.tar.gz -C $PWD/data/original/
tar -xf $PWD/data/compressed/CU-NLP.tar.gz -C $PWD/data/original/
tar -xf $PWD/data/compressed/stita.tar.gz -C $PWD/data/original/
tar -xf $PWD/data/compressed/DigiKlausur.tar.gz -C $PWD/data/original/
