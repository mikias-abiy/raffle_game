DROP TABLE IF EXISTS `raffle_games`;
DROP TABLE IF EXISTS `raffles`;

CREATE TABLE `raffles` (
  `id` varchar(256) NOT NULL,
  `unique_id` varchar(256) NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  PRIMARY KEY (`id`)
);

CREATE TABLE `raffle_games` (
  `id` varchar(256) NOT NULL,
  `raffle_id` varchar(256) NOT NULL,
  `winner_id` varchar(256) NOT NULL,
  `gift_name` varchar(256) NOT NULL,
  `total_gifts`  int(11) NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`raffle_id`) REFERENCES raffles(`id`)
);