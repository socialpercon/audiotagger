from audiotagger.utils.utils import TagUtils


class ExcelTagger(object):
    def __init__(self, logger, input_data):
        self.log = logger
        self.input_data = input_data

        self.metadata = input_data.get_metadata()
        self.modified_metadata = self._apply_modifiers()

    def _apply_modifiers(self):
        modified_metadata = self.metadata
        return modified_metadata

    def save_tags_to_audio_files(self):
        metadata = self.modified_metadata
        if self.input_data.is_dry_run:
            self.log.info("Dry run... saving to {out_file}.")
            TagUtils.dry_run(df=self.modified_metadata,
                              prefix=self.__str__())
            self.log.info("Data saved to {out_file}")
            return

        tag_dict = TagUtils.metadata_to_tags(df_metadata=metadata)
        for k in tag_dict:
            self.log.info(f"Saving {tag_dict[k]} to {k}")
            tag_dict[k].save(k)
