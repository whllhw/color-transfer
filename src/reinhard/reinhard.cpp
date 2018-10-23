// this file original copy from https://github.com/takahiro-itazuri/color-transfer-between-images/blob/master/src/main.cpp
#include<iostream>
#include<cmath>
#include<opencv2/opencv.hpp>
using namespace std;
using namespace cv;
const float eps = 1.0e-5;

// cv::Vec3d BGR2lab(cv::Vec3d bgr) {
// 	cv::Vec3d LMS, lab;
// 	double L = 0.3811 * bgr[2] + 0.5783 * bgr[1] + 0.0402 * bgr[0];
// 	double M = 0.1967 * bgr[2] + 0.7244 * bgr[1] + 0.0782 * bgr[0];
// 	double S = 0.0241 * bgr[2] + 0.1288 * bgr[1] + 0.8444 * bgr[0];
// 	LMS[0] = L > eps ? std::log10(L) : std::log10(eps);
// 	LMS[1] = M > eps ? std::log10(M) : std::log10(eps);
// 	LMS[2] = S > eps ? std::log10(S) : std::log10(eps);

// 	lab[0] = 1 / std::sqrt(3) * (LMS[0] + LMS[1] + LMS[2]);
// 	lab[1] = 1 / std::sqrt(6) * (LMS[0] + LMS[1] - 2 * LMS[2]);
// 	lab[2] = 1 / std::sqrt(2) * (LMS[0] - LMS[1]);

// 	return lab;
// }

// cv::Vec3d lab2BGR(cv::Vec3d lab) {
// 	cv::Vec3d LMS, bgr;
// 	double L = 1 / std::sqrt(3) * lab[0] + 1 / std::sqrt(6) * lab[1] + 1 / std::sqrt(2) * lab[2];
// 	double M = 1 / std::sqrt(3) * lab[0] + 1 / std::sqrt(6) * lab[1] - 1 / std::sqrt(2) * lab[2];
// 	double S = 1 / std::sqrt(3) * lab[0] - 2 / std::sqrt(6) * lab[1];

// 	LMS[0] = L > -5 ? std::pow(10, L) : eps;
// 	LMS[1] = M > -5 ? std::pow(10, M) : eps;
// 	LMS[2] = S > -5 ? std::pow(10, S) : eps;

// 	bgr[0] = 0.0497 * LMS[0] - 0.2439 * LMS[1] + 1.2045 * LMS[2];
// 	bgr[1] = -1.2186 * LMS[0] + 2.3809 * LMS[1] - 0.1624 * LMS[2];
// 	bgr[2] = 4.4679 * LMS[0] - 3.5873 * LMS[1] + 0.1193 * LMS[2];

// 	return bgr;
// }
Vec3d mean(Mat &mat){
	Vec3d avg(0,0,0);
	for (int y = 0, H = mat.rows; y < H; ++y) {
		for (int x = 0, W = mat.cols; x < W; ++x) {
			Vec3b* buf = &mat.at<Vec3b>(y, x);
			avg[0] += (*buf)[0];
			avg[1] += (*buf)[1];
			avg[2] += (*buf)[2];
		}
	}
	for (int c = 0; c < 3; ++c) {
		avg[c] /= avg.rows * avg.cols;
	}
    cout << avg << endl;
	return avg;
}
Vec3d Mat_std(Mat &src_lab,Vec3d &src_avg){
	Vec3d src_sd(0,0,0);
	for (int y = 0, H = src_lab.rows; y < H; ++y) {
		for (int x = 0, W = src_lab.cols; x < W; ++x) {
			Vec3b* buf = &src_lab.at<Vec3b>(y, x);
			src_sd[0] += ((*buf)[0] - src_avg[0]) * ((*buf)[0] - src_avg[0]);
			src_sd[1] += ((*buf)[1] - src_avg[1]) * ((*buf)[1] - src_avg[1]);
			src_sd[2] += ((*buf)[2] - src_avg[2]) * ((*buf)[2] - src_avg[2]);
		}
	}
	for (int c = 0; c < 3; ++c) {
		src_sd[c] /= src_lab.rows * src_lab.cols;
		src_sd[c] = sqrt(src_sd[c]);
	}
    cout << src_sd << endl;
	return src_sd;
}
unsigned char check(int x){
    if (x<0)return 0;
    if (x>255) return 255;
    return x;
}
extern "C" {
	int reinhard(char* src_file, char* ref_file) {
		cv::Mat src, ref, dst;
		cv::Mat src_lab, ref_lab, dst_lab;
		cv::Vec3d src_avg = 0, src_sd = 0, ref_avg = 0, ref_sd = 0;

		// load source image (BGR)
		src = cv::imread(src_file, cv::IMREAD_COLOR);
		// load reference image (BGR)
		ref = cv::imread(ref_file, cv::IMREAD_COLOR);

        src_lab = cv::Mat(src.size(), CV_8UC3);
		ref_lab = cv::Mat(ref.size(), CV_8UC3);

    	dst = cv::Mat(src.size(), CV_8UC3);
        dst_lab = Mat(src.size(), CV_8UC3);

		// convert uchar -> float
		//src.convertTo(src_bgr, CV_64FC3, 1 / 255.0);
		//ref.convertTo(ref_bgr, CV_64FC3, 1 / 255.0);
		
		// initialization for conversion from BGR to lab
		
		cvtColor(src,src_lab,COLOR_BGR2Lab);
		cvtColor(ref,ref_lab,COLOR_BGR2Lab);
        
		// BGR -> lab
		// for (int y = 0; y < src_bgr.rows; ++y) {
		// 	for (int x = 0; x < src_bgr.cols; ++x) {
		// 		src_lab.at<cv::Vec3d>(y, x) = BGR2lab(src_bgr.at<cv::Vec3d>(y, x));
		// 	}
		// }

		// for (int y = 0; y < ref_bgr.rows; ++y) {
		// 	for (int x = 0; x < ref_bgr.cols; ++x) {
		// 		ref_lab.at<cv::Vec3d>(y, x) = BGR2lab(ref_bgr.at<cv::Vec3d>(y, x));
		// 	}
		// }

		// calculate mean
		src_avg = mean(src_lab);
		ref_avg = mean(ref_lab);

		//calculate standard deviation
		src_sd = Mat_std(src_lab,src_avg);
		ref_sd = Mat_std(ref_lab,ref_avg);

		// initialization for output image

		for (int y = 0; y < dst.rows; ++y) {
			for (int x = 0; x < dst.cols; ++x) {
				cv::Vec3b* buf = &src_lab.at<cv::Vec3b>(y, x);
				int l = ref_sd[0] / src_sd[0] * ((*buf)[0] - src_avg[0]) + ref_avg[0];
				int a = ref_sd[1] / src_sd[1] * ((*buf)[1] - src_avg[1]) + ref_avg[1];
				int b = ref_sd[2] / src_sd[2] * ((*buf)[2] - src_avg[2]) + ref_avg[2];
                
				dst_lab.at<cv::Vec3b>(y, x) = cv::Vec3b(check(l), check(a), check(b));
			}
		}
        cvtColor(dst_lab,dst,COLOR_Lab2BGR);

		imwrite("dst.jpg",dst);

		return 0;
	}
	int test(){
		cout << "reinhard modules loaded."<<endl;
    }
}