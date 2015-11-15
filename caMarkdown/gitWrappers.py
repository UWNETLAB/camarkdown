#IN PROGRESS
import dulwich.repo
import dulwich.objects

def commit(fileNames, message):
    blobs = []
    for fname in fileNames:
        with open(fname, 'r') as f:
            blobs.append(dulwich.objects.Blob.from_file(f))
    tree = dulwich.objects.Tree()
    commit = dulwich.objects.Commit()
    commit.tree = tree.id
