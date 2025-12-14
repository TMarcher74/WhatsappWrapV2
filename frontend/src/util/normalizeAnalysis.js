export function normalizeAnalysis(data) {
  if (!data) return null;

  return {
    users: data.users ?? [],

    // Messages
    totalMessages: data.total_messages ?? {},
    deletedMessages: data.deleted_messages ?? {},
    editedMessages: data.edited_messages ?? {},
    mediaMessages: data.media ?? {},

    // Words / sentences / chars
    wordStats: data.word_character_stats ?? {},

    // Time
    dayFrequency: data.day_frequency ?? {},
    timeFrequency: data.time_frequency ?? {},
    userDayFrequency: data.user_wise_day_frequency ?? {},
    userTimeFrequency: data.user_wise_time_frequency ?? {},

    // Links
    links: data.links ?? {},
    detailedLinks: data.detailed_links ?? {},

    // Mentions
    mentions: data.mentions ?? {},

    // Profanity
    profanityTotal: data.profanity?.total ?? {},
    profanityByUser: data.profanity?.user_wise ?? {},

    // Misc
    topWords: data.top_words ?? [],
    milestones: data.milestones ?? [],
    convos: data.convos ?? []
  };
}
