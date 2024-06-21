from locust import HttpLocust, TaskSet, task
from locust import HttpUser, task, between

class WebsiteUser(HttpUser):
    #wait_time = between(5, 15)

    @task
    def load_main(self):
        self.client.post("/common_factors_classification", 
                        json={"input_text": "Dear Journal,\n\nToday was a bit of a struggle on the iCBT platform. I found myself getting really frustrated with the whole thing. It felt like no matter how hard I tried, I just couldn't seem to navigate the app and website properly. It's like I'm just not as tech-savvy as I should be. It's like I was speaking a whole different language!\n\nI mean, I know I'm not the most tech-savvy person out there, but today really made me feel like I was falling behind. The whole user interface and navigation just felt so overwhelming and confusing. It made me question whether or not I was even capable of using this platform to its fullest potential.\n\nIt's like I struggled so much trying to understand how to use the features and tools that were available. It felt like this barrier between me and actually getting the help that I needed. I wish the platform was a little bit more user-friendly for people like me who aren't super tech-savvy.\n\nOn a completely unrelated note, I did manage to go for a walk at the park today. It was nice to get some fresh air and clear my mind, even if only for a little while.\n\nAnyway, I'll have to make sure to bring this up to my therapist next time. Maybe they can offer some tips or resources to help me navigate the digital platform a bit better.\n\nUntil next time,\n[Your Name]"}
                        , headers={"Content-Type": "application/json"})


# locust --headless -u 10 --host=http://<head-ip>:32165 -f locustfile.py --csv results --csv-full-history --only-summary
#                                      
