import os
import glob
import re
import subprocess

def print_header(texfile):
    texfile.writelines([
        "\\documentclass[12pt]{article}\n",
        "\n",
        "\\usepackage{graphicx}\n",
        "\\usepackage{float}\n",
        "\n",
        "\\usepackage[margin=0in]{geometry}\n",
        "\n",
        "\\begin{document}\n",
        ""
    ])

def print_footer(texfile):
    texfile.write("\\end{document}")


def print_graphics(texfile, imgs):
    for img in imgs:
        texfile.writelines([
            "\t\\begin{figure}\n",
            f"\t\t\\includegraphics[height=\\textheight]{{{img}}}\n",
            "\t\\end{figure}\n",
            "\n"
         ])


def sort_image_list(img_list):
    # re pattern
    pat = r"[a-z]+([0-9]*)\.[png|jpg]"

    # list of tuples of img paths and numbers
    imgs_and_nums = [
        (re.match(pat, os.path.split(img_path)[-1]).group(1), img_path)
        for img_path in img_list
    ]

    # sort by page nums
    sorted_imgs_and_nums = sorted(imgs_and_nums, key=lambda x: x[1])

    # return img paths
    return [
        path
        for num, path in sorted_imgs_and_nums
    ]



if __name__ == "__main__":
    
    import argparse

    parser = arparse.ArgumentParser()
    parser.add_argument(
        "--uname",
        default="ryanjs",
        help="username to prepend to output file name"
    )
    parser.add_argument(
        "--src_dir",
        default=os.path.join(os.getcwd(), "./images/"),
        help="directory to get images from"
    )
    parser.add_argument(
        "--dst_dir",
        default=os.getcwd(),
        help="directory to place pdf and tex file in"
    )
    parser.add_argument(
        "--proj_name",
        default=os.path.split(os.getcwd())[-1],
        help="name of project, to use for output filenames"
    )

    args = parser.parse_args()

    # get path to output tex file
    tex_path = os.path.join(
        args.dst_dir,
        f"{args.uname}_{args.proj_name}.tex"
    )

    # generate image list
    image_list = [*glob.glob(args.src_dir)]

    # sort image list
    sorted_images = sort_image_list(image_list)

    # write to tex file
    with open(tex_path, "w") as texfile:
        # print document header
        print_header(texfile)

        # print include graphics
        print_graphics(texfile, sorted_images)

        # print document footer
        print_footer(texfile)

    # compile latex file
    subprocess.run(["pdflatex", "-output-directory", f"args.dst_dir", f"{tex_path}"])

