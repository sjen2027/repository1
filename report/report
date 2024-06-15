options(repos=c(RStudio='http://rstudio.org/_packages', getOption('repos')))
install.packages('readr')
install.packages('gt')
install.packages('infer')
library('readr')
library(tidyverse)
x = read_tsv('DATA2x02 survey (2022) - Form responses 1.tsv')
old_names = colnames(x)
new_names = c("timestamp","covid_positive","living_arrangements","height","uni_travel_method","uni_travel_listen","spain_budget","feel_overseas","feel_anxious","study_hrs","read_news","study_load","work","lab_zoom","social_media","gender","sleep_time","wake_time","random_number","steak_preference","dominant_hand","normal_advanced","exercise_hrs","employment_hrs","city","weekly_saving","hourly_plan","weeks_behind","assignment_on_time","used_r_before","team_role","data2x02_hrs","social_media_hrs","uni_year","sport","wam","shoe_size","decade_selection")
# overwrite the old names with the new names:
colnames(x) = new_names
# combine old and new into a data frame:
name_combo = bind_cols(New = new_names, Old = old_names)
name_combo %>% gt::gt()
visdat::vis_miss(x)
x = x %>% 
  dplyr::mutate(
    height_clean = readr::parse_number(height),
    height_clean = case_when(
      height_clean <= 2.5 ~ height_clean * 100,
      height_clean <= 9 ~ NA_real_,
      TRUE ~ height_clean
    )
  )
# explain this later
x = x %>% filter(timestamp != "19/08/2022 16:23:31")

# test which data is normally distributed
x_filt = x %>% filter(weeks_behind < 10, !is.na(weeks_behind))
par(mfrow=c(1,2)) 
qqnorm(x_filt$weeks_behind, main='Normal')
qqline(x_filt$weeks_behind)
shapiro.test(x_filt$weeks_behind)
library(ggplot2)
ggplot(data = x_filt, aes(x = weeks_behind)) + geom_histogram(bins = 20)

x= x %>% mutate(
  social_media_clean = tolower(social_media),
  social_media_clean = str_replace_all(social_media_clean, '[[:punct:]]',' '),
  social_media_clean = stringr::word(social_media_clean),
  social_media_clean = case_when(
    stringr::str_starts(social_media_clean,"ins") ~ "instagram",
    stringr::str_starts(social_media_clean,"ti") ~ "tiktok",
    stringr::str_starts(social_media_clean,"mess") ~ "facebook",
    stringr::str_starts(social_media_clean,"n") ~ "none",
    is.na(social_media_clean) ~ "none",
    TRUE ~ social_media_clean
  ),
  social_media_clean = tools::toTitleCase(social_media_clean),
  social_media_clean = forcats::fct_lump_min(social_media_clean, min = 10)
)
x = x %>% 
  mutate(identifier = row_number()) %>% 
  mutate(sport = replace_na(sport, "I Don't Play any Sport"))

library(infer)
install.packages("infer")
t
