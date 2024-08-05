#!/usr/bin/env bash
# 1 a)
out_dir=./data
mkdir $out_dir

# Download the text data and place it in the designated directory
wget -P $out_dir https://raw.githubusercontent.com/levinalex/deutsche_verfassungen/master/grundgesetz/grundgesetz.txt

# 1 b) Select from line 1 to first occurrence of pattern '/^I$', delete everything from first line until one line above first occurrence of pattern '/^I$'
sed '1,/^I$/{/^I$/!d}' $out_dir/grundgesetz.txt > $out_dir/grundgesetz_cropped.txt 

# 1 c) Split grundgesetz.txt at chapter headings (roman numerals)
csplit -z --digits=2  --quiet --prefix=kapitel $out_dir/grundgesetz_cropped.txt '/^[MDCLXIV]\+$/' "{*}"
mv kapitel* $out_dir

# 1 d)
for chapter in "$out_dir"/kapitel*; do
  # Put chapter number and heading on one line, replace whitespace with underscores
  title=$(sed -n '/^[MDCLXIV]\+$/{N;s/\s\+/_/g;p}' "$chapter")
  new_subdir="$out_dir/${title}"
  mkdir -p "$new_subdir"
  csplit -z --quiet --prefix=artikel "$chapter" '/^Artikel.\+[0-9a-z]\+$/' "{*}"
  rm artikel00 # This is the chapter heading
  mv artikel* "$new_subdir"

  for article_file in "$new_subdir"/artikel*; do 
     # Extract article number, removing whitespace between number and possible letter
     article_num=$(sed -n '/^Artikel.\+[0-9a-z]\+$/p' "$article_file" | sed 's/[Artikel[:space:]]//g')
     mv "$article_file" "$new_subdir/$article_num" 
  done
done

# 1 e) Delete unneeded data
rm $out_dir/kapitel* $out_dir/grundgesetz* 

# 1 f)
tar -cvf grundgesetz.tar $out_dir
