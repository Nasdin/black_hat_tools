"""
Takes confessions from reddit
"""
from itertools import cycle

import pandas as pd

from config import SOURCE_CONFESSION_CSV, FINISHED_CONFESSION_CSV

source_dataset_df = pd.read_csv(SOURCE_CONFESSION_CSV)


def confession_generator(checkpoint=50):
    """
    Returns a confession, checkpoint saves every checkpoint
    :return:
    """

    try:
        parsed_confession_log_df = pd.read_csv(FINISHED_CONFESSION_CSV)
    except:
        parsed_confession_log_df = pd.DataFrame(data={"parsed_ids": []})

    newly_parsed = []
    unparsed_confessions = source_dataset_df.loc[
        ~source_dataset_df['id'].isin(parsed_confession_log_df['parsed_ids']), ['selftext', 'id']]

    if unparsed_confessions.shape[0] == 0:
        parsed_confession_log_df = pd.DataFrame(data={"parsed_ids": []})
        unparsed_confessions = source_dataset_df.copy()
    infinite_dataset = cycle(unparsed_confessions.itertuples())

    while True:

        for i in range(checkpoint):
            new_confession_row = next(infinite_dataset)

            newly_parsed.append(new_confession_row.id)
            if pd.isna(new_confession_row.selftext):
                continue
            confession = str(new_confession_row.selftext)
            if confession == '[deleted]' or confession == '[removed]' or confession == " ":
                continue
            confession = confession.replace('\n', ' ')

            yield confession

        # End of checkpoint, time to save.
        parsed_confession_log_df['parsed_ids'] = parsed_confession_log_df['parsed_ids'].append(pd.Series(newly_parsed),
                                                                                               ignore_index=True)
        parsed_confession_log_df.to_csv(FINISHED_CONFESSION_CSV, index=False)
        newly_parsed = []
