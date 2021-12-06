# U-NET-for-Super-Resolution-of-Microscopy-Images
Utilizing U-NET to deconvolve Structured Illumination Microscopy(SIM) Images
![Alt text](mitochondria.png?raw=true "Title")
In this report, we design and implement a U-NET to train an algorithm for Super-Resolution. U-Net was introduced by Olaf Ronneberger et al 2015 in the paper “U-Net: Convolutional Networks for Biomedical Image Segmentation” [1]. U-NET won the 2015 ISBI (International Symposium for Biomedical Images) challenge and since then U-NET remains one of the most popular neural networks in the medical imaging field [2]. Super-Resolution of microscopy images is essential because it enables us to observe details of living cellular structures that we have not been able to before using light microscopy. This tool gives biologists the ability to study living cell behavior at higher apparent magnification (higher resolution). Super-Resolution using Structure Illumination Microscopy (SR-SIM) was mainly introduced by Heintzmann et al (1998) and Gustafsson et al (2000) two decades ago. SR-SIM takes in 15 sample images modulated with structured (patterned) illumination and produces a Super-Resolution output image that has double the resolution of a regular light microscope (Wide-Field Microscope) utilizing a reconstruction algorithm. Applying deep-learning to SR-SIM to improve the traditional method (reconstruction algorithm) of Super-Resolution was explored by Jin et al 2020. Where deep-learning  can reduce the number of required images for Super-Resolution from 15 to 3 while also producing the reconstructed image at a faster speed than the traditional method. More on literature Structured Illumination Micrcopy can be found on Jin et al 2020 [3].


References

[1] https://en.wikipedia.org/wiki/U-Net#cite_note-RFB-1  <br>
[2] https://arxiv.org/abs/1505.04597  <br>
[3] Jin, L., Liu, B., Zhao, F. et al. Deep learning enables structured illumination microscopy with low light levels and enhanced speed. Nat Commun 11, 1934 (2020). https://doi.org/10.1038/s41467-020-15784-x 
