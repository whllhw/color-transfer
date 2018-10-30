// this file original copy from https://github.com/takahiro-itazuri/color-transfer-between-images/blob/master/src/main.cpp
#include<iostream>
#include<cmath>
#include<opencv2/opencv.hpp>
using namespace std;
using namespace cv;
const float eps = 1.0e-5;

cv::Vec3d BGR2lab(cv::Vec3d bgr) {
	cv::Vec3d LMS, lab;
	double L = 0.3811 * bgr[2] + 0.5783 * bgr[1] + 0.0402 * bgr[0];
	double M = 0.1967 * bgr[2] + 0.7244 * bgr[1] + 0.0782 * bgr[0];
	double S = 0.0241 * bgr[2] + 0.1288 * bgr[1] + 0.8444 * bgr[0];
	LMS[0] = L > eps ? std::log10(L) : std::log10(eps);
	LMS[1] = M > eps ? std::log10(M) : std::log10(eps);
	LMS[2] = S > eps ? std::log10(S) : std::log10(eps);

	lab[0] = 1 / std::sqrt(3) * (LMS[0] + LMS[1] + LMS[2]);
	lab[1] = 1 / std::sqrt(6) * (LMS[0] + LMS[1] - 2 * LMS[2]);
	lab[2] = 1 / std::sqrt(2) * (LMS[0] - LMS[1]);

	return lab;
}

cv::Vec3d lab2BGR(cv::Vec3d lab) {
	cv::Vec3d LMS, bgr;
	double L = 1 / std::sqrt(3) * lab[0] + 1 / std::sqrt(6) * lab[1] + 1 / std::sqrt(2) * lab[2];
	double M = 1 / std::sqrt(3) * lab[0] + 1 / std::sqrt(6) * lab[1] - 1 / std::sqrt(2) * lab[2];
	double S = 1 / std::sqrt(3) * lab[0] - 2 / std::sqrt(6) * lab[1];

	LMS[0] = L > -5 ? std::pow(10, L) : eps;
	LMS[1] = M > -5 ? std::pow(10, M) : eps;
	LMS[2] = S > -5 ? std::pow(10, S) : eps;

	bgr[0] = 0.0497 * LMS[0] - 0.2439 * LMS[1] + 1.2045 * LMS[2];
	bgr[1] = -1.2186 * LMS[0] + 2.3809 * LMS[1] - 0.1624 * LMS[2];
	bgr[2] = 4.4679 * LMS[0] - 3.5873 * LMS[1] + 0.1193 * LMS[2];

	return bgr;
}

extern "C" {
	int reinhard(char* src_file, char* ref_file,char* output_file) {
		cv::Mat src, ref, dst;
		cv::Mat src_bgr, src_lab, ref_bgr, ref_lab, dst_bgr, dst_lab;
		cv::Vec3d src_avg = 0, src_sd = 0, ref_avg = 0, ref_sd = 0;

		// load source image (BGR)
		src = cv::imread(src_file, cv::IMREAD_COLOR);
		// load reference image (BGR)
		ref = cv::imread(ref_file, cv::IMREAD_COLOR);

		// convert uchar -> float
		src.convertTo(src_bgr, CV_64FC3, 1 / 255.0);
		ref.convertTo(ref_bgr, CV_64FC3, 1 / 255.0);

		// initialization for conversion from BGR to lab
		src_lab = cv::Mat(src_bgr.size(), CV_64FC3);
		ref_lab = cv::Mat(ref_bgr.size(), CV_64FC3);

		// BGR -> lab
		for (int y = 0; y < src_bgr.rows; ++y) {
			for (int x = 0; x < src_bgr.cols; ++x) {
				src_lab.at<cv::Vec3d>(y, x) = BGR2lab(src_bgr.at<cv::Vec3d>(y, x));
			}
		}

		for (int y = 0; y < ref_bgr.rows; ++y) {
			for (int x = 0; x < ref_bgr.cols; ++x) {
				ref_lab.at<cv::Vec3d>(y, x) = BGR2lab(ref_bgr.at<cv::Vec3d>(y, x));
			}
		}

		// calculate mean
		src_avg = cv::Vec3d(0, 0, 0);
		for (int y = 0, H = src_lab.rows; y < H; ++y) {
			for (int x = 0, W = src_lab.cols; x < W; ++x) {
				cv::Vec3d* buf = &src_lab.at<cv::Vec3d>(y, x);
				src_avg[0] += (*buf)[0];
				src_avg[1] += (*buf)[1];
				src_avg[2] += (*buf)[2];
			}
		}
		for (int c = 0; c < 3; ++c) {
			src_avg[c] /= src_lab.rows * src_lab.cols;
		}

		ref_avg = cv::Vec3d(0, 0, 0);
		for (int y = 0, H = ref_lab.rows; y < H; ++y) {
			for (int x = 0, W = ref_lab.cols; x < W; ++x) {
				cv::Vec3d* buf = &ref_lab.at<cv::Vec3d>(y, x);
				ref_avg[0] += (*buf)[0];
				ref_avg[1] += (*buf)[1];
				ref_avg[2] += (*buf)[2];
			}
		}

		for (int c = 0; c < 3; ++c) {
			ref_avg[c] /= ref_lab.rows * ref_lab.cols;
		}

		//calculate standard deviation
		src_sd = cv::Vec3d(0, 0, 0);
		for (int y = 0, H = src_lab.rows; y < H; ++y) {
			for (int x = 0, W = src_lab.cols; x < W; ++x) {
				cv::Vec3d* buf = &src_lab.at<cv::Vec3d>(y, x);
				src_sd[0] += ((*buf)[0] - src_avg[0]) * ((*buf)[0] - src_avg[0]);
				src_sd[1] += ((*buf)[1] - src_avg[1]) * ((*buf)[1] - src_avg[1]);
				src_sd[2] += ((*buf)[2] - src_avg[2]) * ((*buf)[2] - src_avg[2]);
			}
		}

		for (int c = 0; c < 3; ++c) {
			src_sd[c] /= src_lab.rows * src_lab.cols;
			src_sd[c] = std::sqrt(src_sd[c]);
		}

		ref_sd = cv::Vec3d(0, 0, 0);
		for (int y = 0, H = ref_lab.rows; y < H; ++y) {
			for (int x = 0, W = ref_lab.cols; x < W; ++x) {
				cv::Vec3d* buf = &ref_lab.at<cv::Vec3d>(y, x);
				ref_sd[0] += ((*buf)[0] - ref_avg[0]) * ((*buf)[0] - ref_avg[0]);
				ref_sd[1] += ((*buf)[1] - ref_avg[1]) * ((*buf)[1] - ref_avg[1]);
				ref_sd[2] += ((*buf)[2] - ref_avg[2]) * ((*buf)[2] - ref_avg[2]);
			}
		}

		for (int c = 0; c < 3; ++c) {
			ref_sd[c] /= ref_lab.rows * ref_lab.cols;
			ref_sd[c] = std::sqrt(ref_sd[c]);
		}

		// initialization for output image
		dst = cv::Mat(src.size(), CV_8UC3);
		dst_bgr = cv::Mat(src_bgr.size(), CV_64FC3);

		for (int y = 0; y < dst_bgr.rows; ++y) {
			for (int x = 0; x < dst_bgr.cols; ++x) {
				cv::Vec3d* buf = &src_lab.at<cv::Vec3d>(y, x);
				float l = ref_sd[0] / src_sd[0] * ((*buf)[0] - src_avg[0]) + ref_avg[0];
				float a = ref_sd[1] / src_sd[1] * ((*buf)[1] - src_avg[1]) + ref_avg[1];
				float b = ref_sd[2] / src_sd[2] * ((*buf)[2] - src_avg[2]) + ref_avg[2];

				dst_bgr.at<cv::Vec3d>(y, x) = lab2BGR(cv::Vec3d(l, a, b));
			}
		}

		dst_bgr.convertTo(dst, CV_8UC3, 255.0);

		imwrite(output_file,dst);

		return 0;
	}
	int test(){
		cout << "reinhard modules loaded."<<endl;
	}
}