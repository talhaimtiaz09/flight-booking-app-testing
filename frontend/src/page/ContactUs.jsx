import React from "react";

const ContactUs = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-white px-6 py-16">
      <div className="max-w-4xl mx-auto bg-white shadow-xl rounded-2xl overflow-hidden">
        <div className="grid md:grid-cols-2">
          {/* Left side: Image or color block */}
          <div className="bg-blue-600 text-white p-10 flex flex-col justify-center">
            <h2 className="text-4xl font-bold mb-4">Contact Us</h2>
            <p className="text-lg">
              We’re here to help you with your flight bookings, cancellations,
              and general inquiries.
            </p>
          </div>

          {/* Right side: Contact details */}
          <div className="p-10 space-y-6 text-gray-700">
            <div>
              <h3 className="text-xl font-semibold mb-2">Email</h3>
              <p>support@flynow.com</p>
            </div>

            <div>
              <h3 className="text-xl font-semibold mb-2">Phone</h3>
              <p>+1 (800) 555-BOOK</p>
              <p>Available: Mon–Fri, 9:00 AM – 6:00 PM</p>
            </div>

            <div>
              <h3 className="text-xl font-semibold mb-2">Address</h3>
              <p>
                123 Airway Blvd
                <br />
                Sky City, NY 10001
                <br />
                USA
              </p>
            </div>

            <div>
              <h3 className="text-xl font-semibold mb-2">Follow Us</h3>
              <div className="flex space-x-4 text-blue-600">
                <a href="#" className="hover:underline">
                  Facebook
                </a>
                <a href="#" className="hover:underline">
                  Twitter
                </a>
                <a href="#" className="hover:underline">
                  Instagram
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ContactUs;
