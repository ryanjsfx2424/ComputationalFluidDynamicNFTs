def init_auth():
    '''
    gets twitter authentication token from local file
      inputs:  none
      outputs: auth_str (string)
    '''
    print("begin init_auth")
    auth_str = ""
    with open("git_ignores_me.mp4", "r") as fid:
      for line in fid:
        cur_str = line.split(" = ")[1]
        cur_str = cur_str[1:-2] # remove quotes and newline char

        auth_str += cur_str
      # end for line
    # end with open
    return auth_str

    print("success init_auth")
  # end init_auth