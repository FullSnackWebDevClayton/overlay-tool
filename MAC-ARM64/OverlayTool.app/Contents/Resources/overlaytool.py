import wx
import os
from PIL import Image, ExifTags

def correct_orientation(image):
    try:
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == 'Orientation':
                break
        exif = dict(image._getexif().items())

        if exif[orientation] == 3:
            image = image.rotate(180, expand=True)
        elif exif[orientation] == 6:
            image = image.rotate(270, expand=True)
        elif exif[orientation] == 8:
            image = image.rotate(90, expand=True)
    except (AttributeError, KeyError, IndexError, TypeError):
        pass
    return image

def add_overlay(image_path, overlay_path, output_path):
    base_image = Image.open(image_path)
    base_image = correct_orientation(base_image)
    overlay = Image.open(overlay_path)
    overlay = overlay.resize(base_image.size, Image.Resampling.LANCZOS)
    position = ((base_image.width - overlay.width) // 2, (base_image.height - overlay.height) // 2)
    base_image.paste(overlay, position, overlay)
    base_image.save(os.path.join(output_path, os.path.basename(image_path)))

class ImageOverlayApp(wx.Frame):
    def __init__(self, parent, title):
        super(ImageOverlayApp, self).__init__(parent, title=title, size=(400, 200))
        self.InitUI()

    def InitUI(self):
        panel = wx.Panel(self)

        vbox = wx.BoxSizer(wx.VERTICAL)

        # Source folder
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        self.srcDirPicker = wx.DirPickerCtrl(panel, message="Select Source Folder")
        hbox1.Add(wx.StaticText(panel, label="Source Folder:"), flag=wx.RIGHT, border=8)
        hbox1.Add(self.srcDirPicker, proportion=1)
        vbox.Add(hbox1, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)

        # Output folder
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        self.outDirPicker = wx.DirPickerCtrl(panel, message="Select Output Folder")
        hbox2.Add(wx.StaticText(panel, label="Output Folder:"), flag=wx.RIGHT, border=8)
        hbox2.Add(self.outDirPicker, proportion=1)
        vbox.Add(hbox2, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)

        # Overlay file
        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        self.overlayFilePicker = wx.FilePickerCtrl(panel, message="Select Overlay PNG", wildcard="PNG files (*.png)|*.png")
        hbox3.Add(wx.StaticText(panel, label="Overlay File:"), flag=wx.RIGHT, border=8)
        hbox3.Add(self.overlayFilePicker, proportion=1)
        vbox.Add(hbox3, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)

        # Go Button
        hbox4 = wx.BoxSizer(wx.HORIZONTAL)
        goButton = wx.Button(panel, label='Go')
        goButton.Bind(wx.EVT_BUTTON, self.OnGo)
        hbox4.Add(goButton)
        vbox.Add(hbox4, flag=wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, border=10)

        panel.SetSizer(vbox)

    def OnGo(self, event):
        source_folder = self.srcDirPicker.GetPath()
        output_folder = self.outDirPicker.GetPath()
        overlay_image = self.overlayFilePicker.GetPath()
        if source_folder and output_folder and overlay_image:
            for filename in os.listdir(source_folder):
                if filename.lower().endswith(".jpg") or filename.lower().endswith(".png"):
                    image_path = os.path.join(source_folder, filename)
                    add_overlay(image_path, overlay_image, output_folder)
            wx.MessageBox('Processing Complete', 'Info', wx.OK | wx.ICON_INFORMATION)
        else:
            wx.MessageBox('Please select all paths', 'Error', wx.OK | wx.ICON_ERROR)

def main():
    app = wx.App(False)
    frame = ImageOverlayApp(None, title='Image Overlay Tool')
    frame.Show()
    app.MainLoop()

if __name__ == '__main__':
    main()
