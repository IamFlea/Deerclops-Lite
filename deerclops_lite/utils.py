
# Discord allows maximally 2000 characters. Encoding in that case was UTF-8!  
# If Discord codign monkeys change it to ASCII, then the BUG is possible here!
# However, to prevent some possible bugs and errors in development of this script 
# I reduced it by two. Meow meow. :cat:
BUFFER_LENGTH = 1998
    
def strDecompose(string):
    
    # Main index! 
    idx = 0
    string_length = len(string)
    
    # Skip the dog
    if string_length < BUFFER_LENGTH:
        return [string[idx:]]

    result = []
        
    # Since this is while loop I put here some kind of watchdog 
    # Note that we don't kick the dog
    # Message can be 1 998 000 characters long. 
    meow = 0 
    while True:
        if meow > 1000: 
            # Kova is retard
            raise RecursionError('Too many meows in one loop!') 
        meow += 1

        # Append everything if the buffer is long enough 
        if string_length - idx < BUFFER_LENGTH:
            #print("waat")
            result += [string[idx:]]
            break

        # Get the last index of new line character `\n`
        last_idx = string.rfind('\n', idx, idx + BUFFER_LENGTH)  

        # Did we found the ending character? 
        if last_idx == -1 or last_idx == string_length - 1:
            #print("too")
            # There is still something to parse => remove buffer 
            if last_idx - idx +1 < BUFFER_LENGTH:
                raise MemoryError(f"Can not print message longer than {BUFFER_LENGTH} characters")
            result += [string[idx:]]
            break
        # Append the substring ended with `\n`
        result += [string[idx:last_idx + 1]]
        # Add index
        idx = last_idx + 1
        # Repeat
    # while True ends
    return result
