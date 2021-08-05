class Interaction(object):
    def __init__(self, feat_physical_name, feat_index, other_features=None, scatterplots=None, correlations=None,
                 covariances=None, boxplots=None, statsbycategory=None, statsbycategoryflipped=None,
                 statsforcategory=None, ztests=None, ttests=None, anova=None, stackedbarplots=None, chisquared=None,
                 cramers=None, mantelhchi=None, frequency_table=None, frequencytable_firstrow=None):
        # Feature comparing against all others in the data set
        self.feat_physical_name = feat_physical_name
        self.feat_index = feat_index
        self.other_features = other_features

        # Continuous & continuous
        self.scatterplots = scatterplots
        self.correlations = correlations
        self.covariances = covariances

        # Categorical & continuous
        self.boxplots = boxplots
        self.statsbycategory = statsbycategory
        self.statsbycategoryflipped = statsbycategoryflipped
        self.statsforcategory = statsforcategory
        self.ztests = ztests
        self.ttests = ttests
        self.anova = anova

        # Categorical & categorical
        self.stackedbarplots = stackedbarplots
        self.chisquared = chisquared
        self.cramers = cramers
        self.mantelhchi = mantelhchi
        self.frequency_table = frequency_table
        self.frequencytable_firstrow = frequencytable_firstrow
