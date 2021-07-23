# Problem Set 4A
# Name: <your name here>
# Collaborators:
# Time Spent: x:xx

def get_permutations(sequence):
    '''
    Enumerate all permutations of a given string

    sequence (string): an arbitrary string to permute. Assume that it is a
    non-empty string.  

    You MUST use recursion for this part. Non-recursive solutions will not be
    accepted.

    Returns: a list of all permutations of sequence

    Example:
    get_permutations('abc')
    ['abc', 'acb', 'bac', 'bca', 'cab', 'cba']
    Note: depending on your implementation, you may return the permutations in
    a different order than what is listed here.
    '''
    # Base Case
    if len(sequence) == 1:
        permute = [sequence]
        #   return singleton_list
        return permute
    # Recursion Case
    else:
        prev_letter = sequence[0]
        sequence = sequence[1:]
        permute = get_permutations(sequence)
        permute2 = []
        for words in permute:
            for i in range(len(sequence)+1):
                new_word = words[:i] + prev_letter +words[i:]
                permute2.append(new_word)
        return permute2




if __name__ == '__main__':
#    #EXAMPLE
    example_input = 'abc'
    expected_output = ['abc', 'acb', 'bac', 'bca', 'cab', 'cba']
    example_output = get_permutations(example_input)
    print('Input:', example_input)
    print('Expected Output:',expected_output)
    print('Actual Output:', example_output)
    if example_output.sort() == expected_output.sort():
        print("SUCCESS")
    
#    # Put three example test cases here (for your sanity, limit your inputs
#    to be three characters or fewer as you will have n! permutations for a 
#    sequence of length n)


