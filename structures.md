program     = block* end-line
block       = (line/for-block)*
line        = line-number statement end-of-line
line-number = digit digit? digit? digit?
end-line    = line-number END end-of-line