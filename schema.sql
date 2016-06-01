drop table if exists entries;
create table entries (
  id integer primary key autoincrement,
  'background' text not null,
  'text' text not null,
  'color' text not null,
  'showImage' text not null
);
