from url import urls
import git, os, shutil

class diff():
    def __init__(self):
        self.DIR_NAME = "student_work"
        self.master = os.path.join(self.DIR_NAME,"master")
        self.project_name="DiceDuels"



    def GetCodeFromGithub(self,url,student):

        REMOTE_URL = url
        student_folder = os.path.join(self.DIR_NAME,student)
        try:
            os.stat(student_folder)
        except:
            os.mkdir(student_folder)

        project_folder = os.path.join(self.DIR_NAME,student,self.project_name)
        try:
            os.stat(project_folder)
        except:
            os.mkdir(project_folder)

        if os.path.isdir(project_folder):
            shutil.rmtree(project_folder)

        repo = git.Repo.init(project_folder)
        origin = repo.create_remote('origin',REMOTE_URL)
        origin.fetch()
        origin.pull(origin.refs[0].remote_head)

        print "---- DONE ----"
        return project_folder

    def GetAllEntries(self,repo):#todo change loop to remove redundancies
        for student1,url1 in urls.iteritems():
            for student2,url2 in urls.iteritems():
                print("downlaoded ->",self.GetCodeFromGithub(url1,student1))
                print("downlaoded ->",self.GetCodeFromGithub(url2,student2))

    def CompareTwoEntries(self,entryPath1,entryPath2):
        print entryPath1
        print("------")
        print entryPath2
    def CompareAllEntries(self):
        try:
            os.stat(DIR_NAME)
        except:
            os.mkdir(DIR_NAME)
        if os.path.isdir(self.master):
            shutil.rmtree(self.master)

        os.mkdir(master)
        repo = git.Repo.init(self.master)




d1 = diff()

d1.GetAllEntries("DiceDuels")
