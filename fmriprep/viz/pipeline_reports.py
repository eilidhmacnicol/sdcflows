# -*- coding: utf-8 -*-
"""
Created on Wed Jan 27 14:32:13 2016

@author: craigmoodie
"""
import os.path
import matplotlib as mpl
from nilearn.plotting import plot_anat
from nilearn.plotting import plot_epi
from nilearn.plotting import plot_roi
from nipype.interfaces.fsl import MeanImage
from nipype.interfaces.utility import Function
from nipype.interfaces import utility as niu
from nipype.pipeline import engine as pe
from nipype.pipeline.engine import Workflow, Node
from variables_reports import (data_dir, work_dir, subject_list, plugin,
                               plugin_args)

from twelve_image_report_function_w_error import generate_report

Report_workflow = Workflow(name="Report_workflow")
Report_workflow.base_dir = work_dir

mpl.use('Agg')


def anatomical_overlay(in_file, overlay_file, out_file):
    mask_display = plot_anat(in_file)
    mask_display.add_edges(overlay_file)
    mask_display.dim = -1
    #  mask_display.add_contours(overlay_file)
    #  mask_display.add_overlay(overlay_file)
    mask_display.title(out_file, x=0.01, y=0.99, size=15, color=None,
                       bgcolor=None, alpha=1)
    mask_display.savefig(out_file)
    return os.path.abspath(out_file)


def parcel_overlay(in_file, overlay_file, out_file):
    mask_display = plot_epi(in_file)
    mask_display.add_edges(overlay_file)
    #  mask_display.add_contours(overlay_file)
    #  mask_display.add_overlay(overlay_file)
    mask_display.title(out_file, x=0.01, y=0.99, size=15, color=None,
                       bgcolor=None, alpha=1)
    mask_display.savefig(out_file)
    return os.path.abspath(out_file)


def stripped_brain_overlay(in_file, overlay_file, out_file):
    mask_display = plot_roi(in_file, overlay_file, output_file=out_file,
                            title=out_file, display_mode="ortho", dim=-1)
    #  mask_display.bg_img(overlay_file)
    #  mask_display.title(out_file, x=0.01, y=0.99, size=15, color=None,
    #                     bgcolor=None, alpha=1)
    #  mask_display.display_mode = "yx"
    mask_display
    return os.path.abspath(out_file)


def reports():

    report_workflow = Workflow(name="report_workflow")

    inputnode = pe.Node(niu.IdentityInterface(
        fields=['fmap_mag', 'fmap_mag_brain', 'raw_epi', 'stripped_epi',
                'corrected_epi_mean', 'sbref', 'sbref_brain', 'sbref_brain',
                'sbref_t1', 'corrected_sbref', 't1', 't1_brain', 't1_mni',
                'parcels_t1', 'parcels_native']), name='inputnode')
    outputnode = pe.Node(niu.IdentityInterface(fields=['wm_seg']),
                         name='outputnode')

    #  Condensing 4D Stacks into 3D mean
    fmap_mag_mean = Node(MeanImage(), name="Fieldmap_mean")
    fmap_mag_mean.inputs.output_type = "NIFTI_GZ"
    fmap_mag_mean.inputs.dimension = 'T'

    stripped_epi_mean = Node(MeanImage(), name="Stripped_EPI_mean")
    stripped_epi_mean.inputs.output_type = "NIFTI_GZ"
    stripped_epi_mean.inputs.dimension = 'T'

    #  This isn't working!!!
    raw_epi_mean = Node(MeanImage(), name="Raw_EPI_mean")
    raw_epi_mean.inputs.output_type = "NIFTI_GZ"
    raw_epi_mean.inputs.dimension = 'T'
    fmap_overlay = Node(
        Function(
            input_names=["in_file", "overlay_file", "out_file"],
            output_names=["out_file"],
            function=parcel_overlay
        ),
        name="Fieldmap_to_SBRef_Overlay"
    )
    fmap_overlay.inputs.out_file = "Fieldmap_to_SBRef_Overlay.png"

    fmap_mag_BET = Node(
        Function(
            input_names=["in_file", "overlay_file", "out_file"],
            output_names=["out_file"],
            function=stripped_brain_overlay
        ),
        name="Fieldmap_Mag_BET"
    )
    fmap_mag_BET.inputs.out_file = "Fieldmap_Mag_BET.png"

    EPI_BET_report = Node(
        Function(
            input_names=["in_file", "overlay_file", "out_file"],
            output_names=["out_file"],
            function=stripped_brain_overlay
        ),
        name="EPI_Skullstrip_Overlay"
    )
    EPI_BET_report.inputs.out_file = "EPI_Skullstrip_Overlay.png"

    sbref_unwarp_overlay = Node(
        Function(
            input_names=["in_file", "overlay_file", "out_file"],
            output_names=["out_file"],
            function=anatomical_overlay
        ),
        name="SBRef_Unwarping_Overlay"
    )
    sbref_unwarp_overlay.inputs.out_file = "SBRef_Unwarping_Overlay.png"

    epi_unwarp_overlay = Node(
        Function(
            input_names=["in_file", "overlay_file", "out_file"],
            output_names=["out_file"],
            function=anatomical_overlay
        ),
        name="EPI_Unwarping_Overlay"
    )
    epi_unwarp_overlay.inputs.out_file = "EPI_Unwarping_Overlay.png"

    SBRef_BET = Node(
        Function(
            input_names=["in_file", "overlay_file", "out_file"],
            output_names=["out_file"],
            function=stripped_brain_overlay
        ),
        name="SBRef_BET"
    )
    SBRef_BET.inputs.out_file = "SBRef_BET_Overlay.png"
    T1_SkullStrip = Node(
        Function(
            input_names=["in_file", "overlay_file", "out_file"],
            output_names=["out_file"],
            function=stripped_brain_overlay
        ),
        name="T1_SkullStrip"
    )
    T1_SkullStrip.inputs.out_file = "T1_SkullStrip_Overlay.png"

    '''
    parcels_2_EPI = Node(
        Function(
            input_names=["in_file", "overlay_file", "out_file"],
            output_names=["out_file"],
            function=anatomical_overlay
        ),
        name="Parcels_to_EPI_Overlay"
    )
    parcels_2_EPI.inputs.out_file = "Parcels_to_EPI_Overlay.png"

    parcels_2_T1 = Node(
        Function(
            input_names=["in_file", "overlay_file", "out_file"],
            output_names=["out_file"],
            function=anatomical_overlay
        ),
        name="Parcels_to_T1_Overlay"
    )
    parcels_2_T1.inputs.out_file = "Parcels_to_T1_Overlay.png"

    parcels_2_sbref = Node(
        Function(
            input_names=["in_file", "overlay_file", "out_file"],
            output_names=["out_file"],
            function=anatomical_overlay
        ),
        name="Parcels_to_SBRef"
    )
    parcels_2_sbref.inputs.out_file = "Parcels_to_SBRef_Overlay.png"
    '''

    epi_2_sbref = Node(
        Function(
            input_names=["in_file", "overlay_file", "out_file"],
            output_names=["out_file"],
            function=anatomical_overlay
        ),
        name="Functional_to_SBRef_Overlay"
    )
    epi_2_sbref.inputs.out_file = "Functional_to_SBRef_Overlay.png"

    sbref_2_t1 = Node(
        Function(
            input_names=["in_file", "overlay_file", "out_file"],
            output_names=["out_file"],
            function=anatomical_overlay
        ),
        name="SBRef_to_T1_Overlay"
    )
    sbref_2_t1.inputs.out_file = "SBRef_to_T1_Overlay.png"

    '''
    T1_2_MNI = Node(
        Function(
            input_names=["in_file", "overlay_file", "out_file"],
            output_names=["out_file"],
            function=anatomical_overlay
        ),
        name="T1_to_MNI_Overlay"
    )
    T1_2_MNI.inputs.out_file = "T1_to_MNI_Overlay.png"
    T1_2_MNI.inputs.overlay_file = ("/share/sw/free/fsl/5.0.7/fsl/data/"
                                    "standard/MNI152_T1_2mm_brain.nii.gz")
    '''

    final_pdf = Node(
        Function(
            input_names=[
                "output_file", "first_plot", "second_plot", "third_plot",
                "fourth_plot", "fifth_plot", "sixth_plot", "seventh_plot",
                "eighth_plot", "ninth_plot", "tenth_plot", "eleventh_plot",
                "twelfth_plot"
            ],
            output_names=["output_file"],
            function=generate_report
        ),
        name="Final_pdf"
    )
    final_pdf.inputs.output_file = "Preprocessing_Quality_Report.pdf"

    report_workflow.connect([
        (inputnode, fmap_mag_mean, [("fmap_mag", "in_file")]),
        (inputnode, fmap_overlay, [("fieldmap", "in_file")]),
        (inputnode, fmap_overlay, [("sbref", "overlay_file")]),
        (inputnode, fmap_mag_BET, [("fmap_mag_brain", "in_file")]),
        (fmap_mag_mean, fmap_mag_BET, [("out_file", "overlay_file")]),
        (inputnode, raw_epi_mean, [("raw_epi", "in_file")]),
        (inputnode, stripped_epi_mean, [("stripped_EPI", "in_file")]),
        (stripped_epi_mean, EPI_BET_report, [("out_file", "in_file")]),
        (raw_epi_mean, EPI_BET_report, [("out_file", "overlay_file")]),
        (inputnode, sbref_unwarp_overlay, [("corrected_sbref", "in_file")]),
        (inputnode, sbref_unwarp_overlay, [("sbref", "overlay_file")]),
        (inputnode, SBRef_BET, [("sbref_brain", "in_file")]),
        (inputnode, SBRef_BET, [("sbref", "overlay_file")]),
        (inputnode, T1_SkullStrip, [("t1_brain", "in_file")]),
        (inputnode, T1_SkullStrip, [("t1", "overlay_file")]),
        #  (inputnode, parcels_2_EPI, [("parcels_native", "in_file")]),
        #  (inputnode, parcels_2_EPI, [("corrected_epi_mean", "overlay_file")]),
        #  (inputnode, parcels_2_T1, [("parcels_t1", "in_file")]),
        #  (inputnode, parcels_2_T1, [("t1", "overlay_file")]),
        #  (inputnode, parcels_2_sbref, [("parcels_native", "in_file")]),
        #  prob should use corrected sbref brain mask
        #  (inputnode, parcels_2_sbref, [("corrected_sbref", "overlay_file")]),
        (inputnode, epi_2_sbref, [("corrected_epi_mean", "in_file")]),
        (inputnode, epi_2_sbref, [("corrected_sbref", "overlay_file")]),
        #  (inputnode, sbref_2_t1, [("sbref_t1", "in_file")]),
        (inputnode, sbref_2_t1, [("t1", "overlay_file")]),
        (inputnode, epi_unwarp_overlay, [("corrected_epi_mean", "in_file")]),
        (raw_epi_mean, epi_unwarp_overlay, [("out_file", "overlay_file")]),
        #  (inputnode, T1_2_MNI, [("t1_mni", "in_file")]),
        #  replace sbref to mni and epi to mni with sbref and epi unwarping,
        #  also replace epi to t1 with parcel to sbref
        (fmap_overlay, final_pdf, [("out_file", "first_plot")]),
        (EPI_BET_report, final_pdf, [("out_file", "second_plot")]),
        (SBRef_BET, final_pdf, [("out_file", "third_plot")]),
        (T1_SkullStrip, final_pdf, [("out_file",  "fourth_plot")]),
        (sbref_unwarp_overlay, final_pdf, [("out_file",  "fifth_plot")]),
        (epi_unwarp_overlay, final_pdf, [("out_file",  "sixth_plot")]),
        (epi_2_sbref, final_pdf, [("out_file",  "seventh_plot")]),
        (sbref_2_t1, final_pdf, [("out_file",  "eighth_plot")]),
        #  (T1_2_MNI, final_pdf, [("out_file",  "ninth_plot")]),
        #  (parcels_2_T1, final_pdf, [("out_file",  "tenth_plot")]),
        #  (parcels_2_EPI, final_pdf, [("out_file",  "eleventh_plot")]),
        #  (parcels_2_sbref, final_pdf, [("out_file",  "twelfth_plot")]),
    ])

    return report_workflow

if __name__ == '__main__':
    report_wf = reports()
    report_wf.write_graph()
