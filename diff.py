from url import urls
import git, os, shutil
import subprocess


class diff():
    def __init__(self):
        self.DIR_NAME = "student_work"
        self.master = os.path.join(self.DIR_NAME,"master")
        self.project_name="DiceDuels"
        self.projects={}
        self.students={}
        try:
            os.stat(self.DIR_NAME)
        except:
            os.mkdir(self.DIR_NAME)



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

        self.students[student]=project_folder

        return project_folder

    def GetAllEntries(self,repo):#todo change loop to remove redundancies
        for student1,url1 in urls.iteritems():
            print("downlaoded ->",self.GetCodeFromGithub(url1,student1))

    def CompareTwoEntries(self,branchname1,branchname2):
        print("comparing"+branchname1+"<>"+branchname2)
        with open('out-file.txt', 'w') as f:
            update_branches=subprocess.Popen(["git", "diff", "remotes/"+branchname1+"/master","remotes/"+branchname2+"/master"], stdout=f)
            update_branches.wait()

        #git diff master remotes/b/master



    def CompareAllEntries(self):
        if os.path.isdir(self.master):
            shutil.rmtree(self.master)

        os.mkdir(self.master)
        repo = git.Repo.init(self.master)

        #add branches to master repo
        for student,project_folder in self.students.iteritems():
            print "adding",project_folder
            branch_add_output=subprocess.Popen(["git", "remote", "add", "-f",student,os.path.join(".",project_folder,".git")], stdout=subprocess.PIPE)
            branch_add_output.wait()
            print branch_add_output

        print "fetching latest code for all students from cloned repositories"
        update_branches=subprocess.Popen(["git", "remote", "update"])
        update_branches.wait()


        '''
        #diff all students
        for student1,project_folder1 in self.students.iteritems():
            for student2,project_folder2 in self.students.iteritems():
                self.CompareTwoEntries(student1,student2)
                '''


        #remove branches from master repo
        for student,project_folder in self.students.iteritems():
            print "removing",student
            branch_remove_output=subprocess.Popen(["git", "remote", "rm", student], stdout=subprocess.PIPE)
            branch_remove_output.wait()
            print branch_remove_output
        print self.students


        '''
git remote add -f b path/to/repo_b.git
git remote update
git diff master remotes/b/master
git remote rm b
        '''



d1 = diff()

d1.GetAllEntries("DiceDuels")
d1.CompareAllEntries()
