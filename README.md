# ImageLandmarkMarkedTool

Yeah. It's an image landmark marked tool developed by Python.

![image](https://user-images.githubusercontent.com/88467925/135992898-9d664d95-18c8-4299-8733-1d383ba9b084.png)

Have you noticed the first input line? Here you need to enter the original path of the image, and the file should have two sub-files, one is called "original_images", which is used to store the set of images to be labeled, and the other is called "labeling_images", which will automatically generate a TXT file to store the coordinates you typed.

![image](https://user-images.githubusercontent.com/88467925/135995297-02ffdabc-eb36-4927-9c55-b830227890c5.png)

Once you load the image, you can mark the landmark by clicking on the image. To make it easier for you to check, I'll draw a circle where you click.

Did you notice the right box? That's the feature points you have set, and it also will remind you where to click next. Of course, you can modify the parameter "label_list" to specify the feature points you want in advance.

Below the marker box is the console and the progress bar.

ValueNone: Set the null value, the actual value of NaN to record.
Delete: Delete one record of current image.
ClearAll: Delete all the records of current image.

Once you've finished tagging all the feature points, you can click NEXT to tag the NEXT image. And the records will be saved in "label.txt".
By the way, the program by modifying the file name (Add # at the beginning of the file name) to achieve the function of reading records after interruption.
So you can safely close the program, and the next time you open it, you'll be pleasantly surprised to find that it will pick up where you left off.
