
data = read.table("data.csv", sep="|", header=TRUE)
es = data[data$serie=="es1314",]

bro_home = es[es$teamA_id==209,]
bro_home$home <- rep(1, length(bro_home$match_date))
bro_home$outcome <- "1"
bro_home$outcome[bro_home$scoreA<bro_home$scoreB] <- "2"
bro_home$outcome[bro_home$scoreA==bro_home$scoreB] <- "x"

bro_away = es[es$teamB_id==209,]
bro_away$home <- rep(0, length(bro_away$match_date))
bro_away$outcome <- "2"
bro_away$outcome[bro_away$scoreA>bro_away$scoreB] <- "1"
bro_away$outcome[bro_away$scoreA==bro_away$scoreB] <- "x"

bro <- rbind(bro_home,bro_away)


