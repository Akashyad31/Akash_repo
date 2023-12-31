# -*- coding: utf-8 -*-
"""Dicom.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1nuvMr6g-CIcLPta4nExyUEL2JM-_fl0_
"""

pip install pydicom

import pydicom as pdc
import matplotlib.pyplot as plt
import os

def get_header_and_images(ds):
    """
    Method to get b scan images and corresponding header information
    :param ds: dicom data sequence
    :return: header and images
    """

    # info regarding pixel spacing and eye
    sub_field_spacing_eye = ds.get('SharedFunctionalGroupsSequence', [])

    # Check if the required tags are present, otherwise provide default values
    if sub_field_spacing_eye:
        pix_spacing = sub_field_spacing_eye[0].get((0x0028, 0x9110), [])
        if pix_spacing:
            pixels_dist = pix_spacing[0].get((0x0028, 0x0030), {}).value
            dist = pix_spacing[0].get((0x0018, 0x0050), {}).value
        else:
            pixels_dist = [1, 1]
            dist = 1.0
        eye_info = sub_field_spacing_eye[0].get((0x0020, 0x9071), [])
        if eye_info:
            eye_side = str(eye_info[0].get((0x0020, 0x9072), {}).value)
            if eye_side == 'L':
                eye_side = 'OS'
            else:
                eye_side = 'OD'
        else:
            eye_side = ''
    else:
        pixels_dist = [1, 1]
        dist = 1.0
        eye_side = ''

    header = {'Version': ds.get((0x0008, 0x1090), {}).value,
              'SizeX': ds.get((0x0028, 0x0011), {}).value,
              'NumBScans': ds.get((0x0028, 0x0008), {}).value,
              'SizeZ': ds.get((0x0028, 0x0010), {}).value,
              'ScaleX': pixels_dist[1],
              'Distance': dist,
              'ScaleZ': pixels_dist[0],
              'ScanFocus': '',
              'ScanPosition': eye_side,
              'ExamTime': ds.StudyDate,
              'ScanPattern': '',
              'BScanHdrSize': '',
              'ID': ds.get((0x0020, 0x0010), {}).value,
              'ReferenceID': ds.get((0x0020, 0x0011), {}).value,
              'PID': '',
              'PatientID': ds.get((0x0010, 0x0020), {}).value,
              'Padding': '',
              'DOB': ds.get((0x0010, 0x0030), {}).value,
              'VID': '',
              'VisitID': '',
              'VisitDate': '',
              'GridType': '',
              'GridOffset': '',
              'GridType1': '',
              'GridOffset1': '',
              'ProgID': '',
              'PatientSex': ds.get((0x0010, 0x0040), {}).value,
              'DeviceManufacturer': ds.get((0x0008, 0x0070), {}).value,
              'EmmetropicMagnification': ds.get((0x0022, 0x000a), {}).value,
              'IOP': ds.get((0x0022, 0x000b), {}).value,
              'HorizontalFieldofView': ds.get((0x0022, 0x000c), {}).value,
              'PupilDilated': ds.get((0x0022, 0x000d), {}).value,
              'AxialLength': ds.get((0x0022, 0x0030), {}).value,
              'DepthSpatialResolution': ds.get((0x0022, 0x0035), {}).value}

    images = ds.pixel_array
    return header, images


def get_slo(data_seq_slo):
    """
    Method to get slo information including slo image and header
    :param data_seq_slo: dicom data sequence
    :return: header and slo image
    """

    header_slo = {
              'SizeXSlo': data_seq_slo.Columns,
              'SizeYSlo': data_seq_slo.Rows,
              'ScaleXSlo': data_seq_slo.PixelSpacing[0],
              'ScaleYSlo': data_seq_slo.PixelSpacing[1],
              'FieldSizeSlo': data_seq_slo[0x0022, 0x000c].value}
    slo_image = data_seq_slo.pixel_array
    return header_slo, slo_image


def main_read_dcm_spectralis(dicom_file_name, slo_file_name):
    header_slo = {}
    slo_image = []
    warning = 0

    # Assuming the DICOM and SLO files are already uploaded in the current Colab environment

    # Read the SLO file
    slo_file_path = slo_file_name  # Assuming slo_file_name is in the same directory as the DICOM file
    if os.path.exists(slo_file_path):
        d_seq_slo = pdc.dcmread(slo_file_path)
        header_slo, slo_image = get_slo(d_seq_slo)
    else:
        warning = 2003

    # Read the DICOM file
    d_seq = pdc.dcmread(dicom_file_name)

    header, b_scans = get_header_and_images(d_seq)
    header = {**header, **header_slo}
    return warning, header, b_scans, slo_image

# Example usage:
dicom_file_name = "/00000011.dcm"  # Replace with your DICOM file name
slo_file_name = "/00000010.dcm"    # Replace with your SLO file name

warning, header, b_scans, slo_image = main_read_dcm_spectralis(dicom_file_name, slo_file_name)
print("Warning:", warning)
print("Header:", header)
print("B Scans Shape:", b_scans.shape if b_scans is not None else "No B Scans")
print("SLO Image Shape:", slo_image.shape if slo_image is not None else "No SLO Image")

# Commented out IPython magic to ensure Python compatibility.
def visualize_dicom_images(dicom_file_name):
    # Read the DICOM file
    d_seq = pdc.dcmread(dicom_file_name)

    # Get header and B-scan images
    header, b_scans = get_header_and_images(d_seq)

    # Display B-scan images
    plt.figure(figsize=(50, 8))
    for i in range(b_scans.shape[0]):
        plt.subplot(1, b_scans.shape[0], i + 1)
        plt.imshow(b_scans[i, :, :], cmap='gray')
        plt.title(f'B-Scan {i + 1}')
        plt.axis('off')
    plt.show()
# %matplotlib inline
# Example usage:
dicom_file_name = "/00000011.dcm"  # Replace with your DICOM file name
visualize_dicom_images(dicom_file_name)

# Commented out IPython magic to ensure Python compatibility.
def visualize_dicom_images(dicom_file_name, slo_file_name, figsize_bscan=(18, 8), figsize_slo=(8, 8)):
    # Read the B-scan DICOM file
    d_seq = pdc.dcmread(dicom_file_name)

    # Get header and B-scan images
    header, b_scans = get_header_and_images(d_seq)

    # Display B-scan images
    plt.figure(figsize=figsize_bscan)
    for i in range(b_scans.shape[0]):
        plt.subplot(1, b_scans.shape[0], i + 1)
        plt.imshow(b_scans[i, :, :], cmap='gray')
        plt.title(f'B-Scan {i + 1}')
        plt.axis('off')
    plt.show()

    # Read the SLO DICOM file
    d_seq_slo = pdc.dcmread(slo_file_name)

    # Get header and SLO image
    header_slo, slo_image = get_slo(d_seq_slo)

    # Display SLO image
    plt.figure(figsize=figsize_slo)
    plt.imshow(slo_image, cmap='gray')
    plt.title('SLO Image')
    plt.axis('off')
    plt.show()

# Ensure that plots are displayed within the notebook
# %matplotlib inline

# Example usage:
dicom_file_name = "/00000011.dcm"  # Replace with your B-scan DICOM file name
slo_file_name = "/00000010.dcm"    # Replace with your SLO DICOM file name
visualize_dicom_images(dicom_file_name, slo_file_name, figsize_bscan=(50, 8), figsize_slo=(8, 8))