import os

def batch_files_by_size_with_constraints(directory, batch_sizes, max_batch_sizes):
    # batch_sizes is a list of size thresholds in bytes, such as [1*10**6, 100*10**6, 1*10**9]
    # max_batch_sizes is a list of maximum total sizes for each batch, such as [100*10**6, 1*10**9, 1*10**9]
    batches = [[] for _ in batch_sizes] + [[]] # create empty lists for each batch size plus one for the largest files
    batch_sizes.append(float("inf")) # add infinity as the last threshold
    batch_totals = [0 for _ in batch_sizes] # keep track of the total size of each batch
    for root, dirs, files in os.walk(directory): # walk through the directory tree
        for file in files: # for each file
            file_path = os.path.join(root, file) # get the full path
            file_size = os.path.getsize(file_path) # get the size in bytes
            for i, size in enumerate(batch_sizes): # for each size threshold
                if file_size <= size: # if the file size is less than or equal to the threshold
                    batches[i].append(file_path) # add the file path to the corresponding batch
                    batch_totals[i] += file_size # update the total size of the batch
                    break # stop checking the next thresholds
    # apply the additional constraints
    for i, max_size in enumerate(max_batch_sizes): # for each maximum batch size
        if batch_totals[i] > max_size: # if the batch exceeds the limit
            # split the batch into smaller batches
            sub_batches = []
            sub_batch = []
            sub_total = 0
            for file_path in batches[i]:
                file_size = os.path.getsize(file_path)
                if sub_total + file_size > max_size: # if adding the file would exceed the limit
                    sub_batches.append(sub_batch) # add the sub batch to the list
                    sub_batch = [] # start a new sub batch
                    sub_total = 0 # reset the sub total
                sub_batch.append(file_path) # add the file to the sub batch
                sub_total += file_size # update the sub total
            if sub_batch: # if there is a remaining sub batch
                sub_batches.append(sub_batch) # add it to the list
            batches[i] = sub_batches # replace the original batch with the list of sub batches
            
    # modify the last batch to contain only one file per sub batch
    batches[-1] = [[file_path] for file_path in batches[-1]]
    return batches # return the list of batches
